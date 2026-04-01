from typing import TypedDict, List, Dict, Optional, Any

class visualize_state(TypedDict):

    query: Optional[str]
    result: Optional[List[Dict[str, Any]]]
    chart_type: Optional[str]
    plotly_config: Optional[Dict[str, Any]]