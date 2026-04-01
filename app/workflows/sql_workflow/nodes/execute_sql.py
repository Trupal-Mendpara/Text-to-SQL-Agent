from sqlalchemy import text
from decimal import Decimal  # Add this import
from app.db.database import engine
from app.workflows.sql_workflow.sql_state import sql_state

def execute_sql(state: sql_state) -> sql_state:
    sql = state["sql"]
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.mappings().all()
            
            # --- THE FIX ---
            # Convert RowMappings to standard dicts AND Decimals to floats
            clean_rows = []
            for row in rows:
                clean_row = {}
                for key, value in row.items():
                    if isinstance(value, Decimal):
                        clean_row[key] = float(value)
                    else:
                        clean_row[key] = value
                clean_rows.append(clean_row)

        # Save the clean, standard Python list to the state
        state["result"] = clean_rows
        state["error"] = None
        
    except Exception as e:
        state["error"] = str(e)
        # Assuming you handle the None case for retry in your actual state
        current_retry = state.get("retry") or 0
        state["retry"] = current_retry + 1
        
    return state