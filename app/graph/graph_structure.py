from langgraph.graph import StateGraph, END, START
from app.graph.state import TextToSQL
from app.graph.nodes.schema_fetcher import fetch_schema
from app.graph.nodes.sql_generator import query_to_sql
from app.graph.nodes.execute_sql import execute_sql
from app.graph.nodes.query_planner import query_planner

graph = StateGraph(TextToSQL)

graph.add_node("Schema Fetcher", fetch_schema)
graph.add_node("Query Planner", query_planner)
graph.add_node("SQL Generator", query_to_sql)
graph.add_node("SQL Executor", execute_sql)

graph.add_edge(START, "Schema Fetcher")
graph.add_edge("Schema Fetcher", "Query Planner")
graph.add_edge("Query Planner", "SQL Generator")
graph.add_edge("SQL Generator", "SQL Executor")
graph.add_edge("SQL Executor", END)

workflow = graph.compile()
