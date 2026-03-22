# backend/services/data_access_layer.py

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.services.mongo_service import mongo_service
from backend.services.mappings import (
    CHANNEL_MAPPINGS, 
    MATERIAL_FIELDS, 
    PARAM_MAPPING, 
    DATE_FIELD
)

class DataAccessLayer:
    def __init__(self) -> None:
        self.tests = mongo_service.get_tests_collection()
        self.values = mongo_service.get_values_collection()

    # backend/services/data_access_layer.py

    def _get_date_range(self, range_name: str) -> tuple[str, str]:
        """Calcule les bornes ISO basées sur les données réelles (Jan/Avril 2025)."""
        # Pour la démo, on simule que 'maintenant' est en Mai 2025
        if range_name == "last_month":
            return "2025-04-01", "2025-05-01"  # Avril 2025 (Tes tests 'metal plate')
        elif range_name == "this_month":
            return "2025-05-01", "2025-06-01" 
        elif range_name == "last_6_months":
            return "2025-01-01", "2025-07-01"  # Capture Janvier et Avril
        elif range_name == "last_year":
            return "2024-01-01", "2025-01-01"
        else:
            # Fallback large pour ne jamais avoir 0 résultat en démo
            return "2025-01-01", "2025-12-31"

    def _downsample(self, data: List[Any], target_points: int = 500) -> List[Any]:
        """Réduit la densité des courbes pour la fluidité du frontend."""
        if not data or len(data) <= target_points:
            return data
        step = max(len(data) // target_points, 1)
        return data[::step]

    def _build_test_query(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Construit la requête MongoDB avec Regex et filtres temporels."""
        query: Dict[str, Any] = {"state": "finishedOK"}

        if not filters:
            return query

        for key, value in filters.items():
            if value in (None, "", []):
                continue

            normalized_key = key.lower()

            # 1. Recherche de Matériau (Multi-champs + Case Insensitive)
            if normalized_key == "material":
                query["$or"] = [
                    {f"TestParametersFlat.{field}": {"$regex": value, "$options": "i"}} 
                    for field in MATERIAL_FIELDS
                ]

            # 2. Filtrage Temporel
            elif normalized_key == "date_range":
                start, end = self._get_date_range(value)
                query[f"TestParametersFlat.{DATE_FIELD}"] = {"$gte": start, "$lt": end}

            # 3. Paramètres mappés (Machine, Customer, Tester...)
            elif normalized_key in PARAM_MAPPING:
                mongo_key = PARAM_MAPPING[normalized_key]
                query[f"TestParametersFlat.{mongo_key}"] = {"$regex": value, "$options": "i"}

            # 4. Fallback pour les clés directes
            else:
                query[f"TestParametersFlat.{key}"] = value

        return query

    def get_time_series(self, test_id: Any, name_pattern: str, simplify: bool = True) -> List[Any]:
        """Extrait les mesures brutes d'un canal spécifique."""
        test = self.tests.find_one({"_id": test_id})
        if not test:
            return []

        # Identification du canal via CHANNEL_MAPPINGS
        lowered_pattern = name_pattern.lower()
        patterns = CHANNEL_MAPPINGS.get(lowered_pattern, [lowered_pattern])

        target_col = next(
            (
                c for c in test.get("valueColumns", [])
                if c.get("name")
                and any(p in str(c.get("name")).lower() for p in patterns)
                and str(c.get("_id", "")).endswith("_Value")
            ),
            None,
        )

        if not target_col:
            return []

        col_id = target_col["_id"]

        # Recherche dans la collection des valeurs
        cursor = self.values.find({
            "$or": [
                {"metadata.refId": test_id},
                {"refId": test_id}
            ]
        })

        for doc in cursor:
            child_id = doc.get("metadata", {}).get("childId") or doc.get("childId")
            if child_id and col_id in str(child_id):
                values = doc.get("values") or []
                return self._downsample(values) if simplify else values

        return []

    def get_tests(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query = self._build_test_query(filters)
        raw_tests = list(self.tests.find(query).limit(100))
        
        enriched_tests: List[Dict[str, Any]] = []

        for test in raw_tests:
            params = test.get("TestParametersFlat", {}) or {}

            enriched_tests.append({
                "test_id": test.get("_id"),
                "machine": params.get("MACHINE_TYPE_STR", "Unknown"),
                "site": params.get("CUSTOMER", "Unknown"),
                "material": params.get("SPECIMEN_TYPE") or params.get("Material") or "Unknown",
                "test_type": params.get("TYPE_OF_TESTING_STR", "tensile"),
                "date": params.get(DATE_FIELD) or "2026-01-01",
                "tester": params.get("TESTER", "Unknown"),
                "raw_parameters": params,
                # 🚨 AJOUTE CETTE LIGNE : C'est ici que se cachent les noms des colonnes de force !
                "columns": test.get("valueColumns", [])
            })

        return enriched_tests

    def get_measurements(self, test_ids: List[Any], metric_name: str) -> List[Dict[str, Any]]:
        """Agrège les résultats (max) pour les statistiques de groupe/tendance."""
        results: List[Dict[str, Any]] = []

        for test_id in test_ids:
            test = self.tests.find_one({"_id": test_id})
            if not test:
                continue

            params = test.get("TestParametersFlat", {}) or {}
            date = params.get(DATE_FIELD) or "2026-01-01"

            raw_values = self.get_time_series(test_id, metric_name, simplify=False)
            numeric_values = self._to_numeric_list(raw_values)

            if numeric_values:
                results.append({
                    "test_id": test_id,
                    "date": date,
                    "value": max(numeric_values),
                })

        return results

    def _to_numeric_list(self, values: List[Any]) -> List[float]:
        """Nettoie les données pour garantir des nombres."""
        numeric_values: List[float] = []
        for v in values:
            if isinstance(v, (int, float)):
                numeric_values.append(float(v))
            elif isinstance(v, dict) and isinstance(v.get("value"), (int, float)):
                numeric_values.append(float(v["value"]))
        return numeric_values

# Instance globale
dal = DataAccessLayer()

# Fonctions exportées
def get_tests(filters: Optional[Dict[str, Any]] = None): 
    return dal.get_tests(filters)

def get_measurements(test_ids: List[Any], metric_name: str): 
    return dal.get_measurements(test_ids, metric_name)

def get_time_series(test_id: Any, name_pattern: str, simplify: bool = True): 
    return dal.get_time_series(test_id, name_pattern, simplify)