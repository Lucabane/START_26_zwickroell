# backend/test_orchestration.py
import json
from backend.services.llm_orchestrator import route_user_query
from backend.services.semantic_mapper import semantic_mapper

def test_query(message):
    print(f"\n--- TEST QUERY: '{message}' ---")
    
    # 1. Test du mapping sémantique seul
    material = semantic_mapper.extract_material(message)
    test_type = semantic_mapper.extract_test_type(message)
    date_range = semantic_mapper.extract_date_range(message)
    
    print(f"Sémantique détectée :")
    print(f"  - Matériau : {material}")
    print(f"  - Type : {test_type}")
    print(f"  - Période : {date_range}")

    # 2. Test de l'orchestrateur (Routing + Tool Call)
    tool_call = route_user_query(message)
    print(f"\nTool choisi : {tool_call.tool_name}")
    print(f"Arguments générés : {json.dumps(tool_call.args, indent=2)}")

if __name__ == "__main__":
    # La question clé pour ta démo
    test_query("Show me the tensile steel tests from last month")
    
    # Un test de comparaison pour vérifier le fallback
    test_query("Compare Z05 and Z20 machines for plastic")