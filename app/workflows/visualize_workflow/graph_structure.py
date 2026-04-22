from langgraph.graph import StateGraph,START,END
from app.workflows.visualize_workflow.visualize_state import visualize_state
from app.workflows.visualize_workflow.nodes.generate_chart_config import generate_chart_config
from app.workflows.visualize_workflow.nodes.chart_analyser import chart_analyser
from app.workflows.visualize_workflow.utils import check_chart_type

graph = StateGraph(visualize_state)
graph.add_node("Chart Analyser", chart_analyser)
graph.add_node("Config Generator", generate_chart_config)

graph.add_edge(START, "Chart Analyser")
graph.add_conditional_edges("Chart Analyser", check_chart_type)
graph.add_edge("Config Generator", END)

workflow = graph.compile()