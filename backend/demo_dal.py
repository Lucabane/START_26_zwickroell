print("⏳ Initialisation du script...")
try:
    from services.data_access_layer import dal
    print("✅ Import de la DAL réussi")
except Exception as e:
    print(f"❌ Erreur d'import : {e}")
    exit()

def run_full_demo():
    print("\n" + "="*50)
    print("🚀 DEMO DATA ACCESS LAYER - ZWICK ROELL")
    print("="*50)

    # 1. Recherche par matériau (flexible avec SPECIMEN_TYPE)
    material_to_find = "IPS" 
    print(f"\n🔍 1. Recherche de tests pour : '{material_to_find}'...")
    tests = dal.find_tests({"material": material_to_find})
    
    if not tests:
        print(f"⚠️ Aucun test 'IPS' trouvé. Recherche d'un test quelconque...")
        sample_test = dal.tests.find_one({"state": "finishedOK"})
        if not sample_test:
            print("❌ Base de données vide !")
            return
        tests = [sample_test]

    test_id = tests[0]["_id"]
    print(f"✅ Test sélectionné : {test_id}")

    # 2. Extraction avec les ALIAS (force -> Standard force)
    print("\n📊 2. Extraction des courbes...")
    force_data = dal.get_time_series(test_id, "force")
    strain_data = dal.get_time_series(test_id, "strain")

    if force_data and strain_data:
        print(f"✅ SUCCÈS : Courbes extraites ({len(force_data)} points)")
        print(f"   - Force Max : {max(force_data):.2f} N")
    else:
        print("❌ ÉCHEC : Impossible d'extraire les courbes. Vérifiez les alias.")

    print("\n" + "="*50)

if __name__ == "__main__":
    run_full_demo()