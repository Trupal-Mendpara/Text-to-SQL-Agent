import json
from pymongo import MongoClient
from bson import json_util  
from app.workflows.sql_workflow.sql_state import sql_state
from langchain_core.runnables import RunnableConfig

def mongo_query_executor(state: sql_state, config: RunnableConfig) -> sql_state:
    
    db_url = config.get("configurable", {}).get("db_url")
    
    if not db_url:
        state["error"] = "CRITICAL: No database URL provided to the MongoDB executor."
        return state

    generated_payload = state.get("sql")

    try:
        query_data = json.loads(generated_payload)
        collection_name = query_data.get("collection")
        pipeline = query_data.get("pipeline", [])
        
        if not collection_name:
            raise ValueError("The LLM did not specify a collection to query.")

        client = MongoClient(db_url, serverSelectionTimeoutMS=5000)
        db = client.get_default_database()
        collection = db[collection_name]
        raw_results = list(collection.aggregate(pipeline))
        
        safe_json_string = json_util.dumps(raw_results)

        state["result"] = safe_json_string
        state["error"] = ""
        
        client.close()

    except Exception as e:
        state["error"] = f"MongoDB Execution Failed: {str(e)}"
        current_retry = state.get("retry") or 0
        state["retry"] = current_retry + 1
        
    return state