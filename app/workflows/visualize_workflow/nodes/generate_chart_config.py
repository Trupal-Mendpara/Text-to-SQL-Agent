from app.workflows.llm import llm_sql_planner
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.workflows.visualize_workflow.visualize_state import visualize_state
from decimal import Decimal
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class PlotlyChart(BaseModel):
    data: List[Dict[str, Any]] = Field(
        description="""List of trace objects. 
        - For 'bar' or 'scatter' (line): Use 'x' and 'y'.
        - For 'pie': Use 'labels' (category names) and 'values' (numbers). 
        Do NOT use 'x' and 'y' for pie charts."""
    )
    layout: Dict[str, Any] = Field(
        description="Configuration for the chart layout including 'title'."
    )

parser = JsonOutputParser(pydantic_object=PlotlyChart)

def generate_chart_config(state: visualize_state) -> visualize_state:

    query = state.get("query", "")
    raw_results = state.get("result", [])
    chart_type = state.get("chart_type", "")
    
    if not chart_type:
        state["plotly_config"] = None
        return state

    # Handle MongoDB string results
    if isinstance(raw_results, str):
        import json
        try:
            raw_results = json.loads(raw_results)
        except (json.JSONDecodeError, TypeError):
            state["plotly_config"] = None
            return state

    clean_results = []
    for row in raw_results:
        clean_row = {k: float(v) if isinstance(v, Decimal) else v for k, v in row.items()}
        clean_results.append(clean_row)

    prompt = PromptTemplate(
        input_variables=["query", "clean_results", "chart_type"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template="""
        You are an expert Plotly.js configuration generator.
        The system has analyzed the data and decided that a '{chart_type}' chart is the absolute best visualization for this request.

        Your task is to map the DATASET below into a valid Plotly JSON object

        STRICT PLOTLY MAPPING RULES FOR '{chart_type}':
        - If 'pie': You MUST use 'labels' for the category array and 'values' for the numbers array. Do NOT use x and y.
        - If 'bar', 'line', 'area', or 'scatter': You MUST use 'x' and 'y' for the data arrays.
        - If 'multi_bar': Create multiple trace objects in the "data" array. Set "barmode": "group" in the layout.
        - If the metrics have vastly different scales (e.g., quantity vs revenue): Use a dual y-axis. Set "yaxis": "y2" in the second trace, and add "yaxis2": {{"title": "Secondary Metric", "overlaying": "y", "side": "right"}} in the layout.
        - If 'histogram': Use 'x' for the array of raw values to be binned.

        GENERAL RULES:
        - Include a descriptive "title" in the layout.
        - Ensure axis titles are present and clear (except for pie charts).
        - Extract the exact values from the DATASET and place them directly into the arrays.

        {format_instructions}

        USER QUERY: {query}
        DATASET: {clean_results}
        """
    )

    chain = prompt | llm_sql_planner | parser
    
    try:
        chart_config = chain.invoke({"query": query, "clean_results": clean_results, "chart_type": chart_type})
        
        state["plotly_config"] = chart_config
        return state
        
    except Exception as e:
        print(f"DEBUG - JSON config Generation Error: {str(e)}")
        state["plotly_config"] = None
        return state