import json
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from app.workflows.sql_workflow.sql_state import sql_state
from app.workflows.llm import llm_sql_generator
from langchain_core.prompts import  PromptTemplate

class MongoQueryDefinition(BaseModel):
    collection: str = Field(description="The exact name of the MongoDB collection to query")
    pipeline: list[dict] = Field(description="The MongoDB aggregation pipeline (a list of dictionaries) to satisfy the user's request")

def mongo_query_generator(state: sql_state) -> sql_state:
    user_query = state.get("query")
    schema = state.get("schema")
    plan = state.get("plan")
    error = state.get("error")
    
    parser = JsonOutputParser(pydantic_object=MongoQueryDefinition)
    
    prompt = PromptTemplate(
        input_variables=["plan", "schema", "error"],
        template="""You are a Senior MongoDB Database Administrator.
        
        Error (if any from previous attempts):
        {error}

        Plan:
        {plan}

        Schema:
        {schema}

        If there is an error, carefully analyze it and fix your previous MongoDB pipeline.
        
        Instructions:
        1. Use the plan and schema above to generate a precise MongoDB Aggregation Pipeline.
        2. Only use fields that exist in the schema.
        3. CRITICAL UI REQUIREMENT: The final output will be displayed in a flat, 2D data table. You MUST include a final $project stage in your pipeline to flatten any nested objects or arrays.
        4. CRITICAL QUERY REQUIREMENT: Whenever filtering by a string text value, you MUST use a case-insensitive regex match. Example: {{"field": {{"$regex": "value", "$options": "i"}} }}
        5. DATE QUERY REQUIREMENT: Dates in this database are stored as plain ISO-8601 strings (e.g., "2026-04-15T10:30:00Z"). Do NOT use ISODate(), new Date(), or the {{"$date": ...}} extended JSON syntax. Compare dates using standard string operators against raw formatted string dates. Example: {{"order_date": {{"$gt": "2026-04-10"}}}}
        6. Do not write JavaScript or Python code. Only output the raw JSON list of pipeline stages.
        
        {format_instructions}
        """
    )

    chain = prompt | llm_sql_generator | parser
    
    try:
        response = chain.invoke({
            "schema": schema,
            "format_instructions": parser.get_format_instructions(),
            "plan": plan,
            "error": error
        })
        
        payload = {
            "collection": response["collection"],
            "pipeline": response["pipeline"]
        }
        
        state["sql"] = json.dumps(payload)
        state["error"] = "" 
        
    except Exception as e:
        state["error"] = f"Failed to generate MongoDB pipeline: {str(e)}"
        
    return state