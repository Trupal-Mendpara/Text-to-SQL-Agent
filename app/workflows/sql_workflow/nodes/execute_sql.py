from sqlalchemy import text
from app.db.database import engine
from app.workflows.state import TextToSQL

def execute_sql(state: TextToSQL) -> TextToSQL:
    sql = state["sql"]
    error = state["error"]
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.mappings().all()

        state["result"] = rows
        state["error"] = None
    except Exception as e:
        error = str(e)
        state["error"] = error
        state["retry"] += 1
    return state