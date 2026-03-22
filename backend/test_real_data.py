# Crée un fichier test_real_data.py
from backend.services.data_access_layer import dal

# Test 1 : Recherche médicale (Seringues)
print("\n--- TEST MEDICAL ---")
res_med = dal.get_tests({"material": "Syringe"})
print(f"Seringues trouvées : {len(res_med)}")

# Test 2 : Recherche par norme (Plastique)
print("\n--- TEST PLASTIQUE (ISO) ---")
res_iso = dal.get_tests({"material": "ISO 527"})
print(f"Tests ISO 527 trouvés : {len(res_iso)}")

# Test 3 : La question de démo
print("\n--- TEST DÉMO (Metal + Date) ---")
res_demo = dal.get_tests({"material": "metal", "date_range": "last_month"})
print(f"Métaux en Janvier 2021 : {len(res_demo)}")