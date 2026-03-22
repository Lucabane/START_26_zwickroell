# backend/services/mappings.py

# Champs où l'on peut trouver le nom du matériau dans TestParametersFlat
MATERIAL_FIELDS = [
    "SPECIMEN_TYPE", 
    "Material", 
    "Werkstoff",
    "Headline for the report"
]

# Mapping des noms de canaux (pour matcher le champ 'name' dans valueColumns)
# Indispensable pour extraire les courbes (Force, Allongement, etc.)
CHANNEL_MAPPINGS = {
    "strain": ["strain", "deformation", "dehnung", "elongation"],
    "force": ["force", "kraft", "load"],
    "displacement": ["displacement", "weg", "traverse"],
    "stress": ["stress", "spannung"],
    "time": ["time", "zeit"]
}

# Mapping pour les métadonnées de test (utilisé par le DAL pour le filtrage)
PARAM_MAPPING = {
    "machine": "MACHINE_TYPE_STR",
    "test_type": "TYPE_OF_TESTING_STR",
    "tester": "TESTER",
    "standard": "STANDARD",
    "customer": "CUSTOMER",
    "site": "CUSTOMER",
    "job_no": "JOB_NO"
}

# La clé de date à utiliser dans TestParametersFlat
DATE_FIELD = "Date/Clock time"