from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.workflows.sql_workflow.graph_structure import workflow as sql_graph
from app.workflows.visualize_workflow.graph_structure import workflow as viz_graph

visualize_router = APIRouter(prefix="/ai", tags=["AI"])

class VisualizeRequest(BaseModel):
    thread_id: str

@visualize_router.post("/visualize")
def generate_visualization(state: VisualizeRequest):
    config = {
        "configurable": {"thread_id": state.thread_id},
        "run_name": "Visualization_Workflow"
    }

    saved_state_snapshot = sql_graph.get_state(config)
    sql_state_data = saved_state_snapshot.values
    
    incoming_viz_state = {
        "query": sql_state_data.get("query", "Visualize this data"),
        "result": sql_state_data.get("result", []),
    }

    result = viz_graph.invoke(incoming_viz_state, config=config)
    
    plotly_config = result.get("plotly_config")
    
    if not plotly_config:
        raise HTTPException(
            status_code=500, 
            detail="The AI failed to generate the chart configuration. Please check backend logs."
        )

    return {
        "plotly_config": plotly_config
    }