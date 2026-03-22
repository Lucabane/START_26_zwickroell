# backend/test_real_data_debug.py
import json
from backend.services.data_access_layer import dal

def debug_metal_data():
    print("🔍 DEBUG : Analyse des données 'Metal' sans filtre de date...")
    
    # 1. On cherche TOUS les tests qui matchent "metal" ou "metall"
    # Le DAL utilise un regex, donc on teste une valeur large
    filters = {"material": "metal"}
    results = dal.get_tests(filters)
    
    print(f"\n📊 Nombre total de tests trouvés pour le pattern 'metal' : {len(results)}")
    
    if len(results) > 0:
        print("\n--- LISTE DES 10 PREMIERS TESTS TROUVÉS ---")
        print(f"{'ID':<40} | {'Material':<30} | {'Date'}")
        print("-" * 85)
        
        for t in results[:10]:
            print(f"{str(t['test_id']):<40} | {str(t['material']):<30} | {t['date']}")
            
        # 2. Analyse spécifique des dates pour ajuster le DAL
        dates = [t['date'] for t in results if t['date']]
        if dates:
            print("\n📅 Plage de dates trouvée pour les métaux :")
            print(f"Min: {min(dates)}")
            print(f"Max: {max(dates)}")
    else:
        print("\n❌ Aucun test trouvé avec le mot 'metal'.")
        print("Vérification manuelle d'un échantillon brut de la collection...")
        sample = dal.tests.find_one({"state": "finishedOK"})
        if sample:
            params = sample.get("TestParametersFlat", {})
            print(f"Exemple de SPECIMEN_TYPE en base : {params.get('SPECIMEN_TYPE')}")
            print(f"Exemple de Material en base : {params.get('Material')}")

if __name__ == "__main__":
    debug_metal_data()