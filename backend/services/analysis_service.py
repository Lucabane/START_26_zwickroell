from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List


def compare_two_groups(values_a: List[float], values_b: List[float]) -> Dict[str, Any]:
    mean_a = round(mean(values_a), 2) if values_a else 0.0
    mean_b = round(mean(values_b), 2) if values_b else 0.0
    diff_pct = round(((mean_b - mean_a) / mean_a) * 100, 2) if mean_a else 0.0
    direction = "lower" if diff_pct < 0 else "higher"
    return {
        "mean_a": mean_a,
        "mean_b": mean_b,
        "difference_percent": diff_pct,
        "summary": f"Group B is {abs(diff_pct)}% {direction} than Group A.",
        "n_a": len(values_a),
        "n_b": len(values_b),
    }


def summarize_tests_data(tests: List[Dict[str, Any]]) -> Dict[str, Any]:
    machines = sorted({t["machine"] for t in tests})
    sites = sorted({t["site"] for t in tests})
    materials = sorted({t["material"] for t in tests})
    test_types = sorted({t["test_type"] for t in tests})
    return {
        "total_tests": len(tests),
        "machines": machines,
        "sites": sites,
        "materials": materials,
        "test_types": test_types,
    }


def analyze_trend(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(rows, key=lambda r: r["date"])
    values = [float(r["value"]) for r in ordered]
    trend = "stable"
    slope = 0.0
    if len(values) >= 2:
        slope = round((values[-1] - values[0]) / (len(values) - 1), 2)
        if slope > 0.5:
            trend = "increasing"
        elif slope < -0.5:
            trend = "decreasing"
    return {
        "trend": trend,
        "slope": slope,
        "points": ordered,
        "summary": f"The metric shows a {trend} trend over the selected period.",
    }
