# backend/tools/ai_tools.py
from services.data_access_layer import dal

def get_test_list(material: str = None, customer: str = None):
    """
    Recherche des tests dans la base de données. 
    Permet de filtrer par matériau (ex: 'IPS') ou par client.
    Utile pour répondre à : 'Quels sont les tests pour le client X ?'
    """
    filters = {}
    if material: filters['material'] = material
    if customer: filters['customer'] = customer
    return dal.find_tests(filters)

def get_test_analysis(test_id: str):
    """
    Analyse un test précis et retourne ses statistiques (Force Max, etc.)
    et ses métadonnées. C'est l'outil principal de l'IA pour 'comprendre' un test
    sans avoir à lire tous les points de la courbe.
    """
    summary = dal.get_test_summary(test_id)
    force_points = dal.get_time_series(test_id, "force", simplify=False)
    
    if not force_points:
        return {"summary": summary, "analysis": "Aucune donnée de force disponible."}

    analysis = {
        "max_force_N": round(max(force_points), 2),
        "min_force_N": round(min(force_points), 2),
        "avg_force_N": round(sum(force_points) / len(force_points), 2),
        "data_points_count": len(force_points)
    }
    
    return {
        "summary": summary,
        "analysis": analysis
    }

def get_raw_curve_data(test_id: str, data_type: str = "force"):
    """
    Récupère les points (x,y) de la courbe. 
    À utiliser UNIQUEMENT si l'utilisateur demande explicitement les valeurs brutes.
    """
    return dal.get_time_series(test_id, data_type)