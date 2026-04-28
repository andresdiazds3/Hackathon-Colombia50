import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.database import init_db

from app.services.aiService import AIService
from app.tools.orders import generate_work_order, get_work_order, get_all_work_orders, WorkOrderRequest
from app.tools.agent_tools import (
    get_network_summary,
    get_anomalous_access_points,
    get_strategic_recommendations
)

load_dotenv()

app = FastAPI(title="Hackathon Colombia50 - Backend API")

# Inicializamos la base de datos de tickets al arrancar
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("OPENROUTER_API_KEY")
if api_key is None:
    api_key = "dummy_key"

agente = AIService(api_key=api_key)

class ChatRequest(BaseModel):
    question: str

@app.get("/api/dashboard/summary")
def get_dashboard_summary_route():
    """
    Devuelve conteos globales de estado y lista resumida de APs.
    TODO: Persona 1 debe integrar su lógica real. Por ahora usa los mocks de agent_tools.
    """
    return get_network_summary()

@app.get("/api/anomalies")
def get_anomalies_route():
    """
    Devuelve APs con disconnection_rate > 1.3.
    TODO: Persona 1 debe integrar su lógica real. Por ahora usa los mocks de agent_tools.
    """
    return get_anomalous_access_points()

@app.post("/api/work-orders")
def create_work_order_route(req: WorkOrderRequest):
    """
    Genera una orden de trabajo para un AP detectado con problemas.
    """
    order = generate_work_order(
        ap_name=req.ap_name,
        issue_type=req.issue_type,
        priority=req.priority,
        reason=req.reason
    )
    return {"message": "Orden de trabajo generada", "order": order}

@app.get("/api/work-orders/{order_id}")
def read_work_order_route(order_id: str):
    """
    Consulta una orden generada temporalmente.
    """
    order = get_work_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
    return {"order": order}

@app.get("/api/work-orders")
def get_all_work_orders_route(region: Optional[str] = Query(None, description="Filtra las órdenes por región")):
    """
    Consulta todas las órdenes de trabajo, con soporte para filtrar por región.
    Ejemplo: /api/work-orders?region=Montebello
    """
    orders = get_all_work_orders(region)
    return {"orders": orders}

@app.get("/api/recommendations")
def get_recommendations_route():
    """
    Devuelve recomendaciones priorizadas para actuar.
    TODO: Persona 1 debe integrar su lógica real. Por ahora usa los mocks de agent_tools.
    """
    return get_strategic_recommendations()

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """
    Endpoint de chat inteligente. El modelo se encarga de todo el formato del texto final
    haciendo llamadas a las funciones provistas (tools).
    """
    respuesta = await agente.procesar_pregunta(req.question)
    return {
        "question": req.question,
        "answer": respuesta
    }