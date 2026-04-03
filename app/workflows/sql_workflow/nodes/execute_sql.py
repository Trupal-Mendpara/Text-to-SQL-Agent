from sqlalchemy import create_engine, text
from decimal import Decimal
from app.workflows.sql_workflow.sql_state import sql_state
from langchain_core.runnables import RunnableConfig

# Notice we added `config: dict` to the parameters!
def execute_sql(state: sql_state, config: RunnableConfig) -> sql_state:
    sql = state["sql"]
    
    # 1. Unpack the secure URL from LangGraph's config backpack
    db_url = config.get("configurable", {}).get("db_url")
    
    if not db_url:
        state["error"] = "CRITICAL: No database URL provided to the execution node."
        return state

    # 2. Create a dynamic, isolated engine just for this specific request
    engine = create_engine(db_url)
    
    try:
        # 3. Connect, execute, and fetch
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.mappings().all()

            clean_rows = []
            for row in rows:
                clean_row = {}
                for key, value in row.items():
                    # Brilliant handling of JSON serialization issues!
                    if isinstance(value, Decimal):
                        clean_row[key] = float(value)
                    else:
                        clean_row[key] = value
                clean_rows.append(clean_row)

        state["result"] = clean_rows
        state["error"] = None
        
    except Exception as e:
        state["error"] = str(e)
        current_retry = state.get("retry") or 0
        state["retry"] = current_retry + 1
        
    # The 'with' block ends here, instantly closing the database connection.
    # The 'engine' variable is deleted from memory when the function returns.
    return state