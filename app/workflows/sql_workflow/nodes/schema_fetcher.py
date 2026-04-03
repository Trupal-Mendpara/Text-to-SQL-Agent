from sqlalchemy import create_engine, text
from app.workflows.sql_workflow.sql_state import sql_state
from langchain_core.runnables import RunnableConfig

# 1. Added config: RunnableConfig to grab the URL
def schema_fetcher(state: sql_state, config: RunnableConfig) -> sql_state:
    
    # 2. Pull the db_url out of the config backpack
    db_url = config.get("configurable", {}).get("db_url")
    
    if not db_url:
        state["error"] = "CRITICAL: No database URL provided to the schema fetcher."
        return state

    # 3. Create the ephemeral engine for this exact user
    engine = create_engine(db_url)
    
    schema_lines = ["Tables:"]
    try:
        # 4. Connect using our temporary engine
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
        # Save the error to the state instead of returning a completely new dictionary
        state["error"] = f"Error in schema fetching: {str(e)}"
        return state

    # 5. Save the perfectly formatted schema string to the state
    schema_text = "\n".join(schema_lines)
    state["schema"] = schema_text
    
    # The engine vanishes automatically here!
    return state