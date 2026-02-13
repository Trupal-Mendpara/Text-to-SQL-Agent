from sqlalchemy import text
from app.db.database import engine
from app.graph.state import TextToSQL

def execute_sql(state: TextToSQL) -> TextToSQL:
    sql = state["sql"]

    if not sql:
        state["result"] = []
        return state

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.mappings().all()

    state["result"] = rows
    return state