from sqlalchemy import text
from app.db.database import engine
from app.workflows.sql_workflow.sql_state import sql_state

def schema_fetcher(state : sql_state) -> sql_state:
    schema_lines = ["Tables:"]
    try:
        with engine.connect() as conn:
            tables = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)).fetchall()

            for (table_name,) in tables:
                columns = conn.execute(text("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = :table AND table_schema = 'public'
                """), {"table": table_name}).fetchall()

                cols = ", ".join([col[0] for col in columns])
                schema_lines.append(f"{table_name}({cols})")
    except Exception as e:
        return {"Error in schema fetching": str(e)}

    schema_text = "\n".join(schema_lines)
    state["schema"] = schema_text
    return state