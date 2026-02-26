from fastapi import APIRouter
from pydantic import BaseModel
from app.workflows.sql_workflow.graph_structure import workflow

query_router = APIRouter(prefix="/ai", tags=["AI"])

class QueryRequest(BaseModel):
    query: str

@query_router.post("/query", description="Post a query to get the SQL query and the result")
def generate_sql(req: QueryRequest):
    state = {
        "query": req.query,
        "schema": None,
        "sql": None,
        "result": None,
        "plan": None,
        "error": None,
        "retry": -1
    }

    result = workflow.invoke(state)

    return {
        "query": result["query"],
        "schema": result["schema"],
        "plan": result["plan"],
        "generated_sql": result["sql"],
        "result": result["result"],
        "error": result["error"],
        "retry": result["retry"],
    }
