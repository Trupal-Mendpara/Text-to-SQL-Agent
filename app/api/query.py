import uuid
from langgraph.checkpoint.memory import MemorySaver
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.workflows.sql_workflow.graph_structure import workflow

query_router = APIRouter(prefix="/ai", tags=["AI"])

memory = MemorySaver()

class QueryRequest(BaseModel):
    query: str
    db_type: str
    db_url: str                
    thread_id: Optional[str] = None 

@query_router.post("/query", description="Post a query to get the SQL query and the result")
def generate_sql(req: QueryRequest):

    active_thread_id = req.thread_id if req.thread_id else str(uuid.uuid4())
    config = {
        "configurable": {
            "thread_id": active_thread_id,
            "db_url": req.db_url  
        },
        "run_name": "SQL_Generation_Workflow" 
    }

    state = {
        "query": req.query,
        "db_type": req.db_type,
        "schema": None,
        "sql": None,
        "result": None,
        "plan": None,
        "error": None,
        "retry": -1
    }

    try:
        result = workflow.invoke(state, config=config)

        return {
            "query": result.get("query"),
            "schema": result.get("schema"),
            "plan": result.get("plan"),
            "generated_sql": result.get("sql"),
            "result": result.get("result"),
            "error": result.get("error"),
            "retry": result.get("retry"),
            "thread_id": active_thread_id 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))