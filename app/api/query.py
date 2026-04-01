import uuid
from langgraph.checkpoint.memory import MemorySaver
from fastapi import APIRouter
from pydantic import BaseModel
from app.workflows.sql_workflow.graph_structure import workflow

query_router = APIRouter(prefix="/ai", tags=["AI"])

memory = MemorySaver()

class QueryRequest(BaseModel):
    query: str

@query_router.post("/query", description="Post a query to get the SQL query and the result")
def generate_sql(req: QueryRequest):

    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {"thread_id": thread_id},
        "run_name": "SQL_Generation_Workflow" 
    }

    state = {
        "query": req.query,
        "schema": None,
        "sql": None,
        "result": None,
        "plan": None,
        "error": None,
        "retry": -1
    }

    result = workflow.invoke(state, config=config)

    return {
        "query": result["query"],
        "schema": result["schema"],
        "plan": result["plan"],
        "generated_sql": result["sql"],
        "result": result["result"],
        "error": result["error"],
        "retry": result["retry"],
        "thread_id": thread_id
    }
