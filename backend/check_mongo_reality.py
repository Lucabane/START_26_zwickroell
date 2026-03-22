from pymongo import MongoClient
import json

def inspect_vitals():
    # 1. Connexion (Vérifie si l'URI correspond à ton mongo_service.py)
    client = MongoClient("mongodb://localhost:27017/")
    db = client["txp_clean"]
    
    print("--- COLLECTIONS DISPONIBLES ---")
    print(db.list_collection_names())

    # 2. Inspection d'un test
    print("\n--- SAMPLE DOCUMENT: _tests ---")
    # On cherche un test fini pour voir la structure complète
    test_sample = db["_tests"].find_one({"state": "finishedOK"})
    if test_sample:
        # On n'affiche que les clés de premier niveau et un aperçu des paramètres
        print(f"ID: {test_sample.get('_id')}")
        print(f"Keys: {list(test_sample.keys())}")
        print("\nAperçu TestParametersFlat (5 premières clés):")
        params = test_sample.get("TestParametersFlat", {})
        for k in list(params.keys())[:5]:
            print(f"  {k}: {params[k]}")
        
        print("\nAperçu valueColumns (1er canal):")
        if test_sample.get("valueColumns"):
            print(f"  {test_sample['valueColumns'][0]}")
    else:
        print("Aucun document trouvé dans _tests avec state: finishedOK")

    # 3. Inspection d'une colonne de valeurs
    print("\n--- SAMPLE DOCUMENT: valuecolumns_migrated ---")
    val_sample = db["valuecolumns_migrated"].find_one()
    if val_sample:
        print(f"Keys: {list(val_sample.keys())}")
        if "metadata" in val_sample:
            print(f"Metadata keys: {list(val_sample['metadata'].keys())}")
        # Vérification du lien refId
        print(f"RefId exemple: {val_sample.get('metadata', {}).get('refId') or val_sample.get('refId')}")
    else:
        print("Aucun document trouvé dans valuecolumns_migrated")

if __name__ == "__main__":
    inspect_vitals()