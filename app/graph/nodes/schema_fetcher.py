from sqlalchemy import text
from app.db.database import engine
from app.graph.state import TextToSQL

def fetch_schema(state : TextToSQL) -> TextToSQL:
    schema_lines = ["Tables:"]

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
                WHERE table_name = :table
            """), {"table": table_name}).fetchall()

            cols = ", ".join([col[0] for col in columns])
            schema_lines.append(f"{table_name}({cols})")

    schema_text = "\n".join(schema_lines)
    state["schema"] = schema_text
    return state