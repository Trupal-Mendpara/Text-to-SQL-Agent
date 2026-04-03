import uuid
from langgraph.checkpoint.memory import MemorySaver
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.workflows.sql_workflow.graph_structure import workflow

query_router = APIRouter(prefix="/ai", tags=["AI"])

# In-memory checkpointer (Note: use Postgres/Redis for production!)
memory = MemorySaver()

# 1. UPDATE THE PYDANTIC MODEL
# We must accept the db_url from the frontend, and we should optionally
# accept a thread_id so the frontend can maintain a continuous chat session.
class QueryRequest(BaseModel):
    query: str
    db_url: str                # Required! The frontend must send this.
    thread_id: Optional[str] = None # Optional, but recommended for memory.

@query_router.post("/query", description="Post a query to get the SQL query and the result")
def generate_sql(req: QueryRequest):

    # 2. THE MEMORY FIX
    # If the frontend sent a thread_id, use it! Otherwise, generate a new one.
    active_thread_id = req.thread_id if req.thread_id else str(uuid.uuid4())

    # 3. THE BACKPACK FIX (The LangGraph Config)
    # We securely pack the db_url into the config here. It does NOT go into the state!
    config = {
        "configurable": {
            "thread_id": active_thread_id,
            "db_url": req.db_url  # <-- Your execute_sql node will grab this!
        },
        "run_name": "SQL_Generation_Workflow" 
    }

    # 4. INITIALIZE THE STATE
    state = {
        "query": req.query,
        "schema": None,
        "sql": None,
        "result": None,
        "plan": None,
        "error": None,
        "retry": -1
    }

    try:
        # 5. INVOKE THE GRAPH
        result = workflow.invoke(state, config=config)

        # 6. RETURN THE RESULTS safely using .get() to avoid KeyErrors
        return {
            "query": result.get("query"),
            "schema": result.get("schema"),
            "plan": result.get("plan"),
            "generated_sql": result.get("sql"),
            "result": result.get("result"),
            "error": result.get("error"),
            "retry": result.get("retry"),
            "thread_id": active_thread_id # Send this back so the frontend can use it for charting!
        }
    except Exception as e:
        # Catch LangGraph execution errors gracefully
        raise HTTPException(status_code=500, detail=str(e))