from typing import Optional, Dict, Any

def get_network_summary(region: Optional[str] = None) -> Dict[str, Any]:
    """Devuelve conteos globales de estado y lista resumida de APs, con métricas de impacto social."""
    base_data = {
        "online": 17, 
        "offline": 3, 
        "dormant": 3,
        "total_users_affected": 450,
        "social_impact": "Alto (Afectación a 2 escuelas y 1 centro de salud rural)"
    }
    if region:
        base_data["region_filtered"] = region
        base_data["online"] = 5
        base_data["offline"] = 1
        base_data["total_users_affected"] = 120
    return base_data

def get_anomalous_access_points(threshold: float = 1.3, region: Optional[str] = None) -> Dict[str, Any]:
    """Devuelve APs con disconnection_rate mayor al threshold."""
    return {
        "anomalies": [
            {
                "ap_name": "072_Hormiguero_AP1", 
                "region": "El Hormiguero (Zona Rural)",
                "disconnection_rate": 1.5, 
                "social_impact_score": 8.5,
                "reason": "Tasa anómala en la última hora, afectando conectividad escolar"
            }
        ]
    }

def get_top_incident_access_points(limit: int = 5, region: Optional[str] = None) -> Dict[str, Any]:
    """Devuelve los Access Points con mayor cantidad de incidentes."""
    return {
        "aps": [
            {
                "ap_name": "072_Hormiguero_AP1", 
                "region": "El Hormiguero",
                "incidents": 15,
                "affected_community": "Estudiantes y agricultores"
            },
            {
                "ap_name": "067_Montebello-AP1", 
                "region": "Montebello",
                "incidents": 8,
                "affected_community": "Centro de salud local"
            }
        ]
    }

def get_strategic_recommendations(region: Optional[str] = None) -> Dict[str, Any]:
    """Devuelve recomendaciones priorizadas para actuar, basándose en el impacto social."""
    return {
        "recommendations": [
            {
                "ap_name": "067_Montebello-AP1", 
                "region": "Montebello",
                "reason": "AP offline en zona de alta vulnerabilidad. Su caída desconecta al centro de salud local.", 
                "priority": "crítica",
                "social_value": "Restablece servicios telemédicos de urgencia."
            },
            {
                "ap_name": "072_Hormiguero_AP1", 
                "region": "El Hormiguero",
                "reason": "Alta tasa de desconexión durante horario escolar.", 
                "priority": "alta",
                "social_value": "Garantiza el acceso a plataformas educativas de 120 niños."
            }
        ]
    }
