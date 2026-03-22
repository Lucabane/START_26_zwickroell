from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict

from backend.models.schemas import FinalAnswer, ToolCall
from backend.services.openai_client import get_model_name, get_openai_client
from backend.services.semantic_mapper import (
    extract_all_machines,
    extract_material,
    normalize_date_range,
    normalize_metric,
    normalize_test_type,
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an industrial materials test-data assistant for ZwickRoell.
Select exactly one tool and return valid JSON only. 

Available tools:
- find_tests: General search.
- summarize_tests: Statistical summary.
- compare_groups: Benchmark materials or machines.
- trend_analysis: Time-series evolution.
- inspect_data_samples: Reveal raw JSON structure and column names for a material.

Rules:
- For comparisons, use 'material' as group_by if comparing substances like 'metal' vs 'bar'.
- If the user is unsure about field names or column units, use 'inspect_data_samples'.
"""

def _build_local_args(message: str, tool_name: str) -> Dict[str, Any]:
    args: Dict[str, Any] = {}
    msg_lower = message.lower()
    
    # 1. Extractions sémantiques universelles
    material = extract_material(message)
    machines = extract_all_machines(message)
    metric = normalize_metric(message) or "Maximum force"
    date_range = normalize_date_range(message)
    test_type = normalize_test_type(message)

    # 2. Logique spécifique par outil
    if tool_name == "compare_groups":
        args["metric"] = metric
        # On active TOUJOURS la normalisation pour le Golden Path
        args["normalize_units"] = True 
        
        # Cas spécifique : Comparaison de matériaux (Metal vs Bar)
        if any(w in msg_lower for w in ["metal", "plate"]) and "bar" in msg_lower:
            args["group_by"] = "material"
            args["group_a"], args["group_b"] = "metal plate", "BAR 52"
            args["material"] = "metal plate|BAR 52"
        # Cas spécifique : Comparaison de machines
        elif len(machines) >= 2:
            args["group_by"] = "machine"
            args["group_a"], args["group_b"] = machines[0], machines[1]
        else:
            args["group_by"] = "machine"
            args["group_a"], args["group_b"] = "Static", "ProLine"
            args["material"] = material or "metal plate"

    elif tool_name == "find_tests":
        args["material"] = material or "metal plate"
        # Extraction de la limite (ex: "show me 10 tests")
        limit_match = re.search(r'(\d+)\s*(?:tests?|records?|exemples?)', msg_lower)
        args["limit"] = int(limit_match.group(1)) if limit_match else 5
        if test_type: args["test_type"] = test_type
        if date_range: args["date_range"] = date_range

    elif tool_name == "trend_analysis":
        args["material"] = material or "metal plate"
        args["metric"] = metric
        args["date_range"] = date_range or "last_6_months"

    else:
        # Pour inspect_data_samples et summarize_tests
        # Sécurité : On force 'material' pour éviter le crash Pydantic
        args["material"] = material or "metal plate"
        if date_range: args["date_range"] = date_range
        if len(machines) == 1: args["machine"] = machines[0]
    
    return args

def _fallback_route(message: str) -> ToolCall:
    text = message.lower()
    
    if any(word in text for word in ["inspect", "structure", "fields", "columns", "schema"]):
        tool_name = "inspect_data_samples"
    elif any(word in text for word in ["compare", "vs", "difference"]):
        tool_name = "compare_groups"
    elif "normalize" in text or "re-analyze" in text:
        tool_name = "compare_groups"
    elif any(word in text for word in ["trend", "evolution"]):
        tool_name = "trend_analysis"
    elif any(word in text for word in ["summary", "stats", "average"]):
        tool_name = "summarize_tests"
    else:
        tool_name = "find_tests"
    
    return ToolCall(tool_name=tool_name, args=_build_local_args(message, tool_name))

def route_user_query(message: str) -> ToolCall:
    client = get_openai_client()
    if client is None: return _fallback_route(message)

    try:
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            response_format={ "type": "json_object" }
        )
        payload = json.loads(response.choices[0].message.content)
        t_name = payload.get("tool_name")
        if not t_name: return _fallback_route(message)
            
        # Fusion : Le mapper local a la priorité pour corriger les hallucinations
        local_args = _build_local_args(message, t_name)
        merged_args = {**payload.get("args", {}), **local_args}
        
        return ToolCall(tool_name=t_name, args=merged_args)
    except Exception as e:
        logger.error(f"🚨 LLM Error: {e}")
        return _fallback_route(message)

def format_final_answer(user_message: str, tool_call: ToolCall, tool_result: Dict[str, Any]) -> FinalAnswer:
    summary = tool_result.get("summary") or "Analysis complete."
    
    if tool_call.tool_name == "compare_groups":
        diff = abs(tool_result.get("evidence", {}).get("difference_percent", 0))
        if diff > 1000:
            follow_up = "The gap is significant. Would you like to normalize units (kN to N) and re-analyze?"
        else:
            follow_up = "Would you like to see the trend over time for these results?"
            
    elif tool_call.tool_name == "find_tests":
        follow_up = "Would you like a statistical summary of these results?"
        
    elif tool_call.tool_name == "inspect_data_samples":
        follow_up = "Now that we see the field names, should I compare the Standard force across machines?"
    
    else:
        follow_up = "How else can I assist with your production data?"

    return FinalAnswer(answer=summary, suggested_follow_up=follow_up)