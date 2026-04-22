from langgraph.graph import StateGraph, END, START
from app.workflows.sql_workflow.sql_state import sql_state
from app.workflows.sql_workflow.nodes.schema_fetcher import schema_fetcher
from app.workflows.sql_workflow.nodes.sql_generator import sql_generator
from app.workflows.sql_workflow.nodes.execute_sql import execute_sql
from app.workflows.sql_workflow.nodes.query_planner import query_planner
from app.workflows.sql_workflow.nodes.mongo_schema_fetcher import mongo_schema_fetcher
from app.workflows.sql_workflow.nodes.mongo_query_generator import mongo_query_generator
from app.workflows.sql_workflow.nodes.mongo_query_executor import mongo_query_executor
from app.workflows.sql_workflow.nodes.mongo_query_planner import mongo_query_planner
from app.workflows.sql_workflow.utils import error_handler,validate_query,check_db_type,mongo_error_handler,mongo_validate_query
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph = StateGraph(sql_state)

graph.add_node("Schema Fetcher", schema_fetcher)
graph.add_node("Query Planner", query_planner)
graph.add_node("SQL Generator", sql_generator)
graph.add_node("SQL Executor", execute_sql)
graph.add_node("Mongo Schema Fetcher", mongo_schema_fetcher)
graph.add_node("Mongo Query Planner", mongo_query_planner)
graph.add_node("Mongo Query Generator", mongo_query_generator)
graph.add_node("Mongo Query Executor", mongo_query_executor)

graph.add_conditional_edges(START, check_db_type)

graph.add_edge("Schema Fetcher", "Query Planner")
graph.add_conditional_edges("Query Planner",validate_query)
graph.add_edge("SQL Generator", "SQL Executor")
graph.add_conditional_edges("SQL Executor", error_handler)

graph.add_edge("Mongo Schema Fetcher", "Mongo Query Planner")
graph.add_conditional_edges("Mongo Query Planner", mongo_validate_query)
graph.add_edge("Mongo Query Generator", "Mongo Query Executor")
graph.add_conditional_edges("Mongo Query Executor", mongo_error_handler)

workflow = graph.compile(checkpointer=memory)