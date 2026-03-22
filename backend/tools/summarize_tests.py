from __future__ import annotations

from typing import Any, Dict
from backend.services.analysis_service import summarize_tests_data
from backend.services.data_access_layer import get_tests


def summarize_tests(args: Dict[str, Any]) -> Dict[str, Any]:
    tests = get_tests(args)
    summary = summarize_tests_data(tests)
    return {
        "summary": f"Found {summary['total_tests']} tests across {len(summary['machines'])} machines and {len(summary['sites'])} sites.",
        "evidence": summary,
        "filters": {k: v for k, v in args.items() if v},
        "chart_data": [{"label": m, "value": sum(1 for t in tests if t['machine'] == m)} for m in summary["machines"]],
    }
