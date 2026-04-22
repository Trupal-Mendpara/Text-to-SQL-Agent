from app.workflows.visualize_workflow import visualize_state
from pydantic import BaseModel,Field
from typing import Literal
from langchain_core.output_parsers import JsonOutputParser
from app.workflows.llm import llm_sql_planner
from langchain_core.prompts import PromptTemplate

class ChartDecision(BaseModel):
    chart_type: Literal["bar", "line", "pie", "scatter", "multi_bar", "area", "histogram", "heatmap", "none"] = Field(
        description="The chosen chart type based on the data and query."
    )

parser = JsonOutputParser(pydantic_object=ChartDecision)

def chart_analyser(state : visualize_state) -> visualize_state:

    query = state.get("query", "")
    data = state.get("result", [])
    
    if not data:
        state["chart_type"] = "none"    
        return state

    # Handle MongoDB string results
    if isinstance(data, str):
        import json
        try:
            data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            state["chart_type"] = "none"
            return state

    sample_data = data[:5]
    total_rows = len(data)

    prompt = PromptTemplate(
        input_variables=["query", "total_rows", "sample_data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template="""
        You are an expert Data Visualization Architect.
        Analyze the user's natural language query and the data sample to select the optimal chart type.

        USER QUERY: "{query}"
        TOTAL ROWS: {total_rows}
        DATA SAMPLE: {sample_data}

        DECISION RULES:
        - 'none': If the data is not suitable for visualization or there is no data or only one row.
        - 'line': Use for trends over time/dates.
        - 'area': Use for cumulative totals or showing volume trends over time.
        - 'pie': Use for parts-of-a-whole or percentages (ONLY if total rows <= 10).
        - 'scatter': Use to show correlation between two purely numerical fields.
        - 'histogram': Use if the user asks for the "distribution", "spread", or "frequency" of a single numeric column.
        - 'heatmap': Use for correlation matrices or when data has 2 categorical dimensions and 1 numeric metric.
        - 'multi_bar': Use for comparing two or more distinct numerical metrics side-by-side.
        - 'bar': Use for all other standard categorical comparisons.

        {format_instructions}
        """
    )

    chain = prompt | llm_sql_planner | parser
    
    try:
        decision = chain.invoke({
            "query": query, 
            "total_rows": total_rows, 
            "sample_data": sample_data,
        })

        state["chart_type"] = decision.get("chart_type", "bar")
        
    except Exception as e:
        print(f"DEBUG - LLM Analyzer failed, defaulting to bar. Error: {e}")
        state["chart_type"] = "bar"

    return state