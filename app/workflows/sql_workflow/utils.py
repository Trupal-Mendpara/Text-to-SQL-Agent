from app.workflows.state import TextToSQL

def validate_query(state: TextToSQL) -> TextToSQL:
    plan = state["plan"].strip()
    if plan == "INVALID":
        return END
    elif plan == "UNSAFE":
        return END
    elif plan == "INCOMPLETE":
        return END
    else:
        return "SQL Generator"

def error_handler(state: TextToSQL) -> TextToSQL:
    error = state["error"]
    if error and state["retry"] <= 2:
        return "SQL Generator"
    return END