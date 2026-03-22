# backend/services/semantic_mapper.py
from __future__ import annotations
import re
from typing import Dict, Optional, List

    
class SemanticMapper:
    def __init__(self):
        # MAPPINGS OPTIMISÉS POUR LA DÉMO
        self.MATERIAL_ALIASES = {
            # MÉTAL : Si l'utilisateur dit l'un de ces mots, on cherche le pattern regex dans Mongo
            "metal": "metal|metall|alloy|plate",
            "metall": "metal|metall|alloy|plate",
            "alloy": "metal|metall|alloy",
            "nitinol": "nitinol",
            "steel": "DIN|steel|metal", 
            "acier": "DIN|steel|metal",

            # PLASTIQUE / POLYMÈRE
            "plastic": "plastic|ISO 527|Type|Schulterprobe",
            "polymer": "plastic|ISO 527|Type",
            "rubber": "DIN 53504|Winkelprobe",
            "elastomer": "DIN 53504",

            # MÉDICAL (Basé sur ton dump)
            "medical": "Syringe|Schlauch|barrel",
            "syringe": "Syringe",
            "seringue": "Syringe",
            "tube": "Schlauch|Pipe",

            # TEXTILE
            "textile": "textile|Garn|dtex",
        }
        
        # Le reste de tes dictionnaires (TEST_TYPE_ALIASES, etc.) est parfait
        self.TEST_TYPE_ALIASES = {
            "tensile": "tensile", "traction": "tensile", "compression": "compression",
            "charpy": "charpy", "impact": "charpy",
        }


        self.TEST_TYPE_ALIASES = {
            "tensile": "tensile", "traction": "tensile", "compression": "compression",
            "charpy": "charpy", "impact": "charpy",
        }
        self.DATE_RANGE_ALIASES = {
            "last 6 months": "last_6_months", "6 months": "last_6_months",
            "last month": "last_month", "previous month": "last_month",
            "this month": "this_month", "last year": "last_year",
        }
        self.METRIC_ALIASES = {
            "tensile strength": "tensile_strength", "tensile": "tensile_strength",
            "traction": "tensile_strength", "force": "force", "load": "force",
            "strain": "strain", "elongation": "strain",
        }
        self.GROUP_BY_ALIASES = {
            "machine": "machine", "site": "site", "material": "material", "customer": "customer",
        }

        self.KNOWN_MACHINES = ["Z05", "Z10", "Z20", "Static", "ProLine"]
        self.KNOWN_SITES = ["Ulm", "Zurich", "Berlin"]
        self.KNOWN_CUSTOMERS = ["BMW", "Bosch", "ABB"]

    def _find_alias(self, text: str, mapping: Dict[str, str]) -> Optional[str]:
        if not text: return None
        lower = text.lower()
        for alias, canonical in sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True):
            if alias in lower:
                return canonical
        return None

    # --- LOGIQUE MATÉRIAU ---
    def extract_material(self, text: str) -> Optional[str]:
        alias = self._find_alias(text, self.MATERIAL_ALIASES)
        if alias: return alias
        match = re.search(r"\b([A-Z][A-Za-z]+(?:Plast|X)?\s?\d+)\b", text)
        return match.group(1) if match else None
    
    def normalize_material(self, text: str) -> Optional[str]: return self.extract_material(text)

    # --- LOGIQUE TYPE DE TEST ---
    def extract_test_type(self, text: str) -> Optional[str]:
        return self._find_alias(text, self.TEST_TYPE_ALIASES)
    
    def normalize_test_type(self, text: str) -> Optional[str]: return self.extract_test_type(text)

    # --- LOGIQUE DATE ---
    def extract_date_range(self, text: str) -> Optional[str]:
        return self._find_alias(text, self.DATE_RANGE_ALIASES)
    
    def normalize_date_range(self, text: str) -> Optional[str]: return self.extract_date_range(text)

    # --- LOGIQUE MACHINE / SITE / CUSTOMER ---
    def extract_machine(self, text: str) -> Optional[str]:
        upper = text.upper()
        for m in self.KNOWN_MACHINES:
            if m.upper() in upper: return m
        match = re.search(r"\bZ\d{2}\b", upper)
        return match.group(0) if match else None

    def extract_all_machines(self, text: str) -> List[str]:
        upper = text.upper()
        found = [m for m in self.KNOWN_MACHINES if m.upper() in upper]
        regex_found = re.findall(r"\bZ\d{2}\b", upper)
        return list(dict.fromkeys(found + regex_found))

    def extract_site(self, text: str) -> Optional[str]:
        if not text: return None
        for site in self.KNOWN_SITES:
            if site.lower() in text.lower(): return site
        return None

    def extract_customer(self, text: str) -> Optional[str]:
        if not text: return None
        for customer in self.KNOWN_CUSTOMERS:
            if customer.lower() in text.lower(): return customer
        return None

    # --- LOGIQUE MÉTRIQUES & GROUPES ---
    # --- LOGIQUE MÉTRIQUES & GROUPES ---
    # AJOUTE "self" ICI :
    def normalize_metric(self, message: str) -> str:
        # Pour la démo, Standard force est la colonne la plus stable 
        # qui contient des données pour tous tes matériaux.
        return "Standard force"

    def extract_metric(self, text: str) -> Optional[str]: return self.normalize_metric(text)

    def normalize_group_by(self, text: str) -> Optional[str]:
        return self._find_alias(text, self.GROUP_BY_ALIASES)

# --- INSTANCE GLOBALE ---
semantic_mapper = SemanticMapper()

# --- EXPORTS (Compatibilité totale : Module functions + Class Methods) ---
extract_material = semantic_mapper.extract_material
extract_test_type = semantic_mapper.extract_test_type
extract_date_range = semantic_mapper.extract_date_range
extract_machine = semantic_mapper.extract_machine
extract_all_machines = semantic_mapper.extract_all_machines
extract_site = semantic_mapper.extract_site
extract_customer = semantic_mapper.extract_customer
extract_metric = semantic_mapper.extract_metric

normalize_material = semantic_mapper.normalize_material
normalize_test_type = semantic_mapper.normalize_test_type
normalize_date_range = semantic_mapper.normalize_date_range
normalize_metric = semantic_mapper.normalize_metric
normalize_group_by = semantic_mapper.normalize_group_by