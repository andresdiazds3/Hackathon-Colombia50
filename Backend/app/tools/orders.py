import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.database import get_db_connection

class WorkOrderRequest(BaseModel):
    ap_name: str
    region: Optional[str] = "Desconocida"
    issue_type: str = "anomalía_detectada"
    priority: str = "alta"
    reason: str = "Tasa de desconexión elevada"

def generate_work_order(ap_name: str, issue_type: str, priority: str, reason: str, region: str = "Desconocida") -> dict:
    order_id = str(uuid.uuid4())
    generated_at = datetime.utcnow().isoformat()
    status = "pending"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO work_orders (id, ap_name, region, issue_type, priority, reason, status, generated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (order_id, ap_name, region, issue_type, priority, reason, status, generated_at))
    conn.commit()
    conn.close()

    return {
        "id": order_id,
        "ap_name": ap_name,
        "region": region,
        "issue_type": issue_type,
        "priority": priority,
        "generated_at": generated_at,
        "reason": reason,
        "status": status
    }

def get_work_order(order_id: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute('SELECT * FROM work_orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def get_all_work_orders(region: Optional[str] = None) -> List[Dict]:
    """Obtiene todas las órdenes, opcionalmente filtradas por región."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if region:
        # Busca cualquier región que contenga el texto enviado (ej. "Montebello")
        query = "SELECT * FROM work_orders WHERE region LIKE ? ORDER BY generated_at DESC"
        rows = cursor.execute(query, (f"%{region}%",)).fetchall()
    else:
        rows = cursor.execute('SELECT * FROM work_orders ORDER BY generated_at DESC').fetchall()
        
    conn.close()
    return [dict(row) for row in rows]
