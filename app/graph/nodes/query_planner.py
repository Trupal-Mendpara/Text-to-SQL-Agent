from app.graph.state import TextToSQL
from app.llm import llm_sql_planner
from langchain_core.prompts import PromptTemplate

def query_planner(state: TextToSQL) -> TextToSQL:
    schema = state["schema"]
    query = state["query"]
    
    prompt = PromptTemplate(
        input_variables=["schema", "query"],
        template="""
        You are an expert PostgreSQL developer.

        Use the schema below to plan a SQL SELECT query based on the query provided.

        -Your task is to plan a SQL SELECT query based on the schema provided.
        -Break down the complex query into smaller steps and generate a plan for each step.
        -The plan should be the set of instructions to generate the SQL query.
        -Return only the plan.
        -Don't return the empty plan.

        Schema:
        {schema}

        Query:
        {query}
        """
    )

    chain = prompt | llm_sql_planner
    response = chain.invoke({"schema": schema, "query": query})
    state["plan"] = response.content.strip()
    return state