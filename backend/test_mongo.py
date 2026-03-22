from services.mongo_service import mongo_service

def test_connection():
    try:
        # On essaie de récupérer un seul document pour voir si ça répond
        test_doc = mongo_service.get_tests_collection().find_one()
        if test_doc:
            print("🚀 Connexion réussie !")
            print(f"Exemple de test trouvé : {test_doc.get('name', 'Sans nom')}")
            # Vérifie si TestParametersFlat existe (super important pour la suite)
            params = test_doc.get('TestParametersFlat', {})
            print(f"Paramètres détectés : {list(params.keys())[:5]}...")
        else:
            print("⚠️ Connecté, mais la collection 'Tests' semble vide.")
    except Exception as e:
        print(f"💥 Erreur de connexion : {e}")

if __name__ == "__main__":
    test_connection()