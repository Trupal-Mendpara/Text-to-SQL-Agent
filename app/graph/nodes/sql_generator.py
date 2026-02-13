from langchain_core.prompts import  PromptTemplate
from app.llm import llm_sql_generator
from app.graph.state import TextToSQL

def query_to_sql(state: TextToSQL) -> TextToSQL:

    plan = state["plan"]
    schema = state["schema"]

    prompt = PromptTemplate(
    input_variables=["plan", "schema"],
    template="""
    You are an expert PostgreSQL developer.
    Use the plan and schema below to generate a SQL SELECT query.
    Rules:
    - Generate the SQL query based on only on the plan and schema.
    - Do not write inside '''sql''' or '''SQL''' and just return the query
    Plan:
    {plan}
    Schema:
    {schema}
    Return only SQL.
    """
    )

    chain = prompt | llm_sql_generator
    response = chain.invoke({"plan": plan, "schema": schema})
    state["sql"] = response.content.strip()
    return state