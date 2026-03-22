# backend/api/data.py
from fastapi import APIRouter, HTTPException
from typing import Optional
# 1. Correction de l'import
from backend.services.data_access_layer import dal

router = APIRouter(prefix="/data", tags=["Data Extraction"])

@router.get("/tests") # 2. Correction: router au lieu de app
def list_tests(material: Optional[str] = None):
    """Liste les tests filtrés par matériau (ex: IPS)."""
    # 3. Correction: get_tests au lieu de find_tests
    return dal.get_tests({"material": material} if material else None)

@router.get("/tests/{test_id}")
def get_test_detail(test_id: str):
    """Récupère les détails d'un test spécifique."""
    # On utilise get_tests avec un filtre technique sur l'ID
    results = dal.get_tests({"test_id": test_id})
    if not results:
        raise HTTPException(status_code=404, detail="Test non trouvé")
    return results[0]

@router.get("/tests/{test_id}/curve")
def get_curve(test_id: str, type: str = "force"):
    """Récupère la courbe (force ou strain) pour le graphique."""
    data = dal.get_time_series(test_id, type)
    if not data:
        raise HTTPException(status_code=404, detail=f"Courbe '{type}' non trouvée")
    return {"test_id": test_id, "type": type, "values": data}