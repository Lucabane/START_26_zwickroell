# backend/test_tools_execution.py
import json
from backend.tools.registry import execute_tool

def test_tool_real(name, args):
    print(f"\n--- EXECUTION DU TOOL: {name} ---")
    print(f"Arguments: {json.dumps(args, indent=2)}")
    
    try:
        result = execute_tool(name, args)
        
        print("\n✅ RÉSULTAT OBTENU :")
        print(f"Summary: {result.get('summary')}")
        
        evidence = result.get('evidence', {})
        if name == "find_tests":
            print(f"Nombre de tests trouvés: {evidence.get('count')}")
        elif name == "compare_groups":
            print(f"Moyenne A: {evidence.get('mean_a')} {evidence.get('unit')}")
            print(f"Moyenne B: {evidence.get('mean_b')} {evidence.get('unit')}")
            print(f"Différence: {evidence.get('difference_percent')}%")

        if result.get('chart_data'):
            print(f"Chart Data: {len(result['chart_data'])} points prêts pour Nathan.")
            
    except Exception as e:
        print(f"\n❌ ERREUR D'EXÉCUTION : {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test 1: La recherche de tests (Ta question de démo)
    test_tool_real("find_tests", {
        "material": "steel",
        "test_type": "tensile",
        "date_range": "last_month"
    })

    # Test 2: La comparaison (Plus complexe, nécessite des mesures)
    test_tool_real("compare_groups", {
        "material": "plastic",
        "metric": "force", # On utilise 'force' car on sait qu'il est mappé dans ton DAL
        "group_by": "machine",
        "group_a": "Static", # Nom vu dans ton diagnostic Mongo
        "group_b": "Z05"
    })