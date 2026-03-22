from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    ChatRequest, ChatResponse, DataUsed, DataFilter, 
    AssistantStat, ToolTraceStep, AssistantChart
)
from backend.services.llm_orchestrator import route_user_query, format_final_answer
from backend.tools.registry import execute_tool

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        # 1. Orchestration & Execution
        tool_call = route_user_query(req.message)
        tool_result = execute_tool(tool_call.tool_name, tool_call.args)
        final_answer = format_final_answer(req.message, tool_call, tool_result)
        
        evidence = tool_result.get("evidence", {})
        charts = []
        display_stats = []

        # 2. LOGIQUE D'AFFICHAGE MULTI-OUTILS (English Labels)
        
        # CAS A : COMPARAISON (Bar Chart + Detail Stats)
        if tool_call.tool_name == "compare_groups":
            if "chart_data" in tool_result:
                charts.append(AssistantChart(
                    type="bar",
                    title=f"Comparison: {tool_call.args.get('metric')}",
                    xLabel="Group",
                    yLabel=evidence.get("unit", "Value"),
                    xKey="label",
                    yKey="value",
                    data=tool_result["chart_data"]
                ))
            
            display_stats = [
                AssistantStat(label="N (A)", value=evidence.get("n_a", 0), description=f"Tests for {tool_call.args.get('group_a')}"),
                AssistantStat(label="N (B)", value=evidence.get("n_b", 0), description=f"Tests for {tool_call.args.get('group_b')}"),
                AssistantStat(label="Average A", value=evidence.get("mean_a", 0)),
                AssistantStat(label="Average B", value=evidence.get("mean_b", 0)),
                AssistantStat(label="Difference", value=f"{evidence.get('difference_percent', 0)}%", description="Relative gap")
            ]

        # CAS B : ANALYSE DE TENDANCE (Line Chart + Trend Stats)
        elif tool_call.tool_name == "trend_analysis":
            if "chart_data" in tool_result:
                charts.append(AssistantChart(
                    type="line", # Changement de type pour l'évolution temporelle
                    title=f"Trend: {tool_call.args.get('metric')} Over Time",
                    xLabel="Date",
                    yLabel=evidence.get("unit", "Value"),
                    xKey="date", # On utilise la date en axe X
                    yKey="value",
                    data=tool_result["chart_data"]
                ))
            
            display_stats = [
                AssistantStat(label="Trend Status", value=evidence.get("trend_direction", "Stable")),
                AssistantStat(label="Total Samples", value=evidence.get("count", 0)),
                AssistantStat(label="Volatility", value=f"{evidence.get('std_dev', 0)}", description="Standard deviation")
            ]

        # CAS C : RECHERCHE & INSPECTION (Simple Stats)
        elif tool_call.tool_name in ["find_tests", "inspect_data_samples"]:
            display_stats = [
                AssistantStat(
                    label="Records shown", 
                    value=evidence.get("count", 0),
                    description="Items displayed in table"
                )
            ]

        # 3. Sidebar DataUsed (Transparency / Side Panel)
        total_db_matches = evidence.get("total_count", evidence.get("count", 0))
        data_used_info = DataUsed(
            testsCount=total_db_matches,
            filters=[
                DataFilter(key="material", value=str(tool_call.args.get("material", "N/A"))),
                DataFilter(key="tool", value=tool_call.tool_name)
            ],
            parameters=[str(tool_call.args.get("metric", "Standard force"))]
        )

        # 4. Final Chat Response Construction
        return ChatResponse(
            answer=final_answer.answer,
            charts=charts,
            stats=display_stats,
            dataUsed=data_used_info,
            nextSteps=[final_answer.suggested_follow_up] if final_answer.suggested_follow_up else [],
            toolUsed=tool_call.tool_name,
            toolTrace=[
                ToolTraceStep(
                    step=1,
                    tool=tool_call.tool_name,
                    purpose="Analyzing production data",
                    inputSummary=str(tool_call.args),
                    outputSummary=f"Scanned {total_db_matches} records successfully."
                )
            ]
        )

    except Exception as e:
        # Le middleware de debug dans main.py affichera le traceback complet
        raise HTTPException(status_code=500, detail=str(e))