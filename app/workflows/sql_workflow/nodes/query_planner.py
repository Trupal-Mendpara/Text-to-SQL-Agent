from app.workflows.state import TextToSQL
from app.workflows.llm import llm_sql_planner
from langchain_core.prompts import PromptTemplate

def query_planner(state: TextToSQL) -> TextToSQL:
    schema = state["schema"]
    query = state["query"]
    
    prompt = PromptTemplate(
        input_variables=["schema", "query"],
        template="""
        Query:
        {query}
        Schema:
        {schema}

        First check whether the user is asking a question that can be answered with a SELECT query, if yes then proceed to the second check and if not then,
        Respond with EXACTLY ONE of the following keywords:
        UNSAFE - The user is asking to change data (e.g., "Delete user 5", "Add a new row", "Drop the table").
        INVALID - The input is gibberish, conversational, or not a data request.
        INCOMPLETE - The input is incomplete.
        Second check if the query is simple or complex.
        if the query is simple:
            return the natural language query itself.
        else:
            return a plan to generate the SQL query and always try to sort the result in descending order if not specified in the query.
        - Don't return sql query in the plan in both cases whether the query is simple or complex.       
        """
    )

    chain = prompt | llm_sql_planner
    response = chain.invoke({"schema": schema, "query": query})
    state["plan"] = response.content.strip()
    return state