from app.workflows.sql_workflow.sql_state import sql_state
from langgraph.graph import END

def validate_query(state: sql_state) -> sql_state:
    plan = state["plan"].strip()
    if plan == "INVALID":
        return END
    elif plan == "UNSAFE":
        return END
    elif plan == "INCOMPLETE":
        return END
    else:
        return "SQL Generator"

def error_handler(state: sql_state) -> sql_state:
    error = state["error"]
    if error and state["retry"] <= 2:
        return "SQL Generator"
    return END