from langchain_core.prompts import  PromptTemplate
from app.workflows.llm import llm_sql_generator
from app.workflows.sql_workflow.sql_state import sql_state

def sql_generator(state: sql_state) -> sql_state:

    plan = state["plan"]
    schema = state["schema"]
    error = state["error"]

    prompt = PromptTemplate(
    input_variables=["plan", "schema", "error"],
    template="""
    Error:
    {error}

    Plan:
    {plan}

    Schema:
    {schema}

    If there is an error, fix the query based on the error.

    Use the plan and schema below to generate a SQL SELECT query.
    Rules:
    - Generate the SQL query based on only on the plan and schema.
    - If query is trying to use WHERE clause and the value is string then use ILIKE operator and also use pattern matching with % operator. 
    - Do not write inside '''sql''' or '''SQL''' and just return the query
    Return only SQL.
    """
    )

    chain = prompt | llm_sql_generator
    response = chain.invoke({"plan": plan, "schema": schema, "error": error})
    state["sql"] = response.content.strip()
    return state