from typing import TypedDict, Optional, List, Dict, Any

class sql_state(TypedDict):
    query: str
    db_type: str
    schema: Optional[str]
    sql: Optional[str]
    result: Optional[List[Dict[str, Any]]]
    plan: Optional[str]
    error: Optional[str]
    retry: Optional[int]