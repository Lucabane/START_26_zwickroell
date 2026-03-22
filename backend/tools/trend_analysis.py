from __future__ import annotations
from typing import Any, Dict
import math
# On garde tes imports d'origine car ils fonctionnent
from backend.services.analysis_service import analyze_trend
from backend.services.data_access_layer import get_measurements, get_tests

def trend_analysis(args: Dict[str, Any]) -> Dict[str, Any]:
    metric = args.get("metric", "Maximum force")
    material = args.get("material", "metal plate")
    
    # 1. Extraction des filtres
    filters = {k: v for k, v in args.items() if k in {"material", "test_type", "machine", "site", "date_range"} and v}
    
    # 2. Récupération des données (Méthode originale pour éviter le crash)
    tests = get_tests(filters)
    if not tests:
        return {
            "summary": f"No data found for {material}.",
            "evidence": {"count": 0, "total_count": 0}
        }
    
    test_ids = [t["test_id"] for t in tests]
    
    # RÉTABLISSEMENT : On récupère les 'rows' avant d'appeler analyze_trend
    # car c'est ce que ton service semble attendre d'après ton code précédent
    rows = get_measurements(test_ids, metric)
    trend = analyze_trend(rows)
    
    points = trend.get("points", [])
    if not points:
        return {"summary": "No measurements found for trend calculation.", "evidence": {"count": 0}}

    # 3. Calcul de volatilité manuel (évite d'installer numpy en urgence)
    values = [p["value"] for p in points]
    mean_val = sum(values) / len(values)
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    std_dev = round(math.sqrt(variance), 2)
    
    # Détection d'instabilité
    is_volatile = std_dev > (mean_val * 0.3) # Seuil 30%
    trend_status = "Volatile" if is_volatile else trend.get("trend", "Stable")

    # 4. Formatage du retour pour chat.py
    return {
        "summary": f"Trend analysis on **{len(points)}** samples shows a **{trend_status.lower()}** behavior.",
        "chart_data": [{"date": p["date"][:10], "value": round(p["value"], 2)} for p in points],
        "evidence": {
            "count": len(points),            # Nécessaire pour les cartes de stats
            "total_count": len(tests),       # Nécessaire pour le sidebar
            "trend_direction": trend_status,
            "std_dev": std_dev,
            "unit": trend.get("unit", "N")
        }
    }