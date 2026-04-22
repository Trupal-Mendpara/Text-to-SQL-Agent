from sqlalchemy import create_engine, inspect
from app.workflows.sql_workflow.sql_state import sql_state
from langchain_core.runnables import RunnableConfig

def schema_fetcher(state: sql_state, config: RunnableConfig) -> sql_state:
    
    db_url = config.get("configurable", {}).get("db_url")
    
    if not db_url:
        state["error"] = "CRITICAL: No database URL provided to the schema fetcher."
        return state

    engine = create_engine(db_url)
    
    schema_lines = ["Tables:"]
    try:
        inspector = inspect(engine)
        
        table_names = inspector.get_table_names()
        
        for table_name in table_names:
            columns = inspector.get_columns(table_name)
            
            cols = ", ".join([col['name'] for col in columns])
            schema_lines.append(f"{table_name}({cols})")
                
    except Exception as e:
        state["error"] = f"Error in schema fetching: {str(e)}"
        return state

    schema_text = "\n".join(schema_lines)
    state["schema"] = schema_text
    
    return state