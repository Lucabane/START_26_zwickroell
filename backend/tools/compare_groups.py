from __future__ import annotations

from typing import Any, Dict, List
from backend.services.analysis_service import compare_two_groups
from backend.services.data_access_layer import get_measurements, get_tests


def compare_groups(args: Dict[str, Any]) -> Dict[str, Any]:
    group_by = args["group_by"]
    metric = args["metric"]
    normalize = args.get("normalize_units", False)

    # 1. Préparation des filtres
    filters_common = {k: v for k, v in args.items() if k in {"material", "test_type", "site", "customer", "date_range"} and v}
    filters_a = dict(filters_common)
    filters_b = dict(filters_common)
    filters_a[group_by] = args["group_a"]
    filters_b[group_by] = args["group_b"]

    # 2. Récupération des données
    tests_a = get_tests(filters_a)
    tests_b = get_tests(filters_b)
    rows_a = get_measurements([t["test_id"] for t in tests_a], metric)
    rows_b = get_measurements([t["test_id"] for t in tests_b], metric)

    values_a = [r["value"] for r in rows_a]
    values_b = [r["value"] for r in rows_b]

    # 3. LOGIQUE DE NORMALISATION (The "Magic" part)
    # If a value is < 100 in a force metric, it's likely kN. We convert to N.
    normalization_applied = False
    if normalize:
        if any(v < 100 for v in values_a) or any(v < 100 for v in values_b):
            values_a = [v * 1000 if v < 100 else v for v in values_a]
            values_b = [v * 1000 if v < 100 else v for v in values_b]
            normalization_applied = True

    # 4. Calcul des statistiques sur les données (potentiellement) normalisées
    stats = compare_two_groups(values_a, values_b)
    
    # Gestion des unités pour l'affichage
    unit = "N" # Default for force
    if "strength" in metric.lower():
        unit = "MPa"
    elif normalization_applied:
        unit = "N (Normalized)"

    # 5. Construction du résumé
    diff_desc = "higher" if stats['difference_percent'] > 0 else "lower"
    summary = f"{args['group_b']} is {abs(stats['difference_percent']):.2f}% {diff_desc} than {args['group_a']} for {metric}."
    
    if normalization_applied:
        summary += " **Note: Units were automatically normalized from kN to N for accuracy.**"

    return {
        "summary": summary,
        "evidence": {
            "n_a": stats["n_a"],
            "n_b": stats["n_b"],
            "mean_a": round(stats["mean_a"], 2),
            "mean_b": round(stats["mean_b"], 2),
            "difference_percent": round(stats["difference_percent"], 2),
            "unit": unit,
        },
        "filters": filters_common,
        "chart_data": [
            {"label": args["group_a"], "value": round(stats["mean_a"], 2)},
            {"label": args["group_b"], "value": round(stats["mean_b"], 2)},
        ],
    }