# backend/tools/registry.py
from __future__ import annotations

from typing import Any, Callable, Dict
from backend.tools.compare_groups import compare_groups
from backend.tools.find_tests import find_tests
from backend.tools.summarize_tests import summarize_tests
from backend.tools.trend_analysis import trend_analysis
# 🚨 AJOUTE CET IMPORT ICI
from backend.tools.inspect_data_samples import execute_inspection 

TOOL_REGISTRY: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "find_tests": find_tests,
    "summarize_tests": summarize_tests,
    "compare_groups": compare_groups,
    "trend_analysis": trend_analysis,
    # 🚨 ENREGISTRE LE NOUVEL OUTIL ICI
    "inspect_data_samples": execute_inspection,
}


def execute_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOL_REGISTRY[tool_name](args)