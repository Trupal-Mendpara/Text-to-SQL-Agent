from app.workflows.visualize_workflow.visualize_state import visualize_state
from langgraph.graph import END

def check_chart_type(state: visualize_state) -> visualize_state:
    type = state["chart_type"].strip()
    if type == "none":
        return END
    else:
        return "Config Generator"