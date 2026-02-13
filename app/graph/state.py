from typing import TypedDict, Optional, List, Dict, Any

class TextToSQL(TypedDict):
    query: str
    schema: Optional[str]
    sql: Optional[str]
    result: Optional[List[Dict[str, Any]]]
    plan: Optional[str]