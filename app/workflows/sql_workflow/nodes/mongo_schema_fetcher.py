from pymongo import MongoClient
from langchain_core.runnables import RunnableConfig
from app.workflows.sql_workflow.sql_state import sql_state

def mongo_schema_fetcher(state: sql_state, config: RunnableConfig) -> sql_state:
    db_url = config.get("configurable", {}).get("db_url")
    print(f"DEBUG RAW URL: {db_url}")
    
    if not db_url:
        state["error"] = "CRITICAL: No database URL provided to the schema fetcher."
        return state
    
    try:
        client = MongoClient(db_url)
        db = client.get_default_database()
        
        schema_lines = ["Collections:"]
        
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            sample_doc = collection.find_one()
            
            if sample_doc:
                fields = ", ".join(sample_doc.keys())
                schema_lines.append(f"{collection_name}({fields})")
            else:
                schema_lines.append(f"{collection_name}(empty)")
                
        client.close()
        
        state["schema"] = "\n".join(schema_lines)
        state["error"] = None
        
    except Exception as e:
        state["error"] = f"Error in MongoDB schema fetching: {str(e)}"
        
    return state