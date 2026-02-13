from fastapi import APIRouter
from pydantic import BaseModel
from app.graph.graph_structure import workflow

router = APIRouter(prefix="/ai", tags=["AI"])

class QueryRequest(BaseModel):
    query: str

@router.post("/query", description="Post a query to get the SQL query and the result")
def generate_sql(req: QueryRequest):
    state = {
        "query": req.query,
        "schema": None,
        "sql": None,
        "result": None,
        "plan": None
    }

    result = workflow.invoke(state)

    return {
        "query": result["query"],
        "schema": result["schema"],
        "plan": result["plan"],
        "generated_sql": result["sql"],
        "result": result["result"]
    }
