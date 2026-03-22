from services.mongo_service import mongo_service

def create_indexes():
    print("⚡ Création des index pour booster la DAL...")
    values = mongo_service.get_values_collection()
    tests = mongo_service.get_tests_collection()

    # Index sur la collection des mesures (LE PLUS IMPORTANT)
    # On indexe refId et childId car ce sont nos clés de recherche
    values.create_index([("refId", 1)]) # Index racine
    values.create_index([("metadata.refId", 1)]) # Index metadata
    
    # Index sur la collection des tests pour la recherche par matériau
    tests.create_index([("TestParametersFlat.Material", 1)])
    tests.create_index([("TestParametersFlat.SPECIMEN_TYPE", 1)])
    
    print("✅ Index créés ! Les recherches seront instantanées.")

if __name__ == "__main__":
    create_indexes()
