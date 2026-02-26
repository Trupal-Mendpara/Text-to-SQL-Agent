from langgraph.graph import StateGraph, END, START
from app.workflows.state import TextToSQL
from app.workflows.sql_workflow.nodes.schema_fetcher import schema_fetcher
from app.workflows.sql_workflow.nodes.sql_generator import sql_generator
from app.workflows.sql_workflow.nodes.execute_sql import execute_sql
from app.workflows.sql_workflow.nodes.query_planner import query_planner
from app.workflows.sql_workflow.utils import error_handler,validate_query

graph = StateGraph(TextToSQL)

graph.add_node("Schema Fetcher", schema_fetcher)
graph.add_node("Query Planner", query_planner)
graph.add_node("SQL Generator", sql_generator)
graph.add_node("SQL Executor", execute_sql)

graph.add_edge(START, "Schema Fetcher")
graph.add_edge("Schema Fetcher", "Query Planner")
graph.add_conditional_edges("Query Planner",validate_query)
graph.add_edge("SQL Generator", "SQL Executor")
graph.add_conditional_edges("SQL Executor", error_handler)

workflow = graph.compile()