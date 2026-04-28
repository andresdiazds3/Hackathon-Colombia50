import json
from typing import Any, cast
from openai import OpenAI

from app.tools.agent_tools import (
    get_network_summary,
    get_access_points_overview,
    get_anomalous_access_points,
    get_top_incident_access_points,
    get_strategic_recommendations,
    classify_failure_type
)
from app.tools.orders import generate_work_order

class AIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        # Lista de modelos gratuitos como fallback
        self.free_models = [
            "google/gemini-2.0-flash-lite-preview-02-05:free",
            "meta-llama/llama-3.1-8b-instruct:free",
            "mistralai/mistral-nemo:free",
            "openrouter/auto"
        ]

    def _call_with_fallback(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] = None):
        """Intenta llamar a la API iterando por los modelos disponibles si hay error."""
        last_error = None
        for model in self.free_models:
            try:
                if tools:
                    return self.client.chat.completions.create(
                        model=model,
                        messages=cast(Any, messages),
                        tools=cast(Any, tools)
                    )
                else:
                    return self.client.chat.completions.create(
                        model=model,
                        messages=cast(Any, messages)
                    )
            except Exception as e:
                print(f"[Fallback] Error con el modelo {model}: {str(e)}")
                last_error = e
                continue
        # Si todos fallan, lanzamos la última excepción
        raise last_error

    async def procesar_pregunta(self, user_message: str) -> str:
        try:
            tools: list[dict[str, Any]] = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_network_summary",
                        "description": "Obtiene un resumen del estado de la red y métricas de impacto social.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "region": {"type": "string", "description": "Región específica (ej. 'Montebello')"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_access_points_overview",
                        "description": "Devuelve la lista completa de todos los Access Points, su distribución y estado actual."
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_anomalous_access_points",
                        "description": "Obtiene APs con comportamiento anómalo y su impacto en la comunidad.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "threshold": {"type": "number", "description": "Umbral de anomalía (ej. 1.3)"},
                                "region": {"type": "string", "description": "Región opcional a filtrar"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_top_incident_access_points",
                        "description": "Obtiene los APs con mayor cantidad de incidentes y las zonas vulnerables afectadas.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "limit": {"type": "integer"},
                                "region": {"type": "string"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_strategic_recommendations",
                        "description": "Obtiene recomendaciones de mantenimiento priorizadas 100% por IMPACTO SOCIAL.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "region": {"type": "string"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "classify_failure_type",
                        "description": "Clasifica el tipo de falla de un AP basándose en sus eventos de red y métricas horarias (intermitente, total, degradada).",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "ap_name": {"type": "string", "description": "Nombre del Access Point a analizar"}
                            },
                            "required": ["ap_name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "generate_work_order",
                        "description": "Genera una orden de trabajo para arreglar un AP.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "ap_name": {"type": "string"},
                                "region": {"type": "string", "description": "Región donde está el AP"},
                                "issue_type": {"type": "string"},
                                "priority": {"type": "string"},
                                "reason": {"type": "string"}
                            },
                            "required": ["ap_name", "issue_type", "priority", "reason"]
                        }
                    }
                }
            ]

            messages: list[dict[str, Any]] = [
                {
                    "role": "system", 
                    "content": "Eres un analista de redes con un fuerte enfoque social. Tu labor es analizar datos técnicos y traducirlos en el impacto real que tienen en las personas (escuelas sin internet, hospitales desconectados). Usa siempre las herramientas para obtener datos precisos por región y responde destacando el valor social de resolver los problemas."
                },
                {"role": "user", "content": user_message}
            ]

            # 1. Primera llamada con fallback
            response = self._call_with_fallback(messages, tools)
            
            # Verificación de seguridad por si OpenRouter devuelve un formato inesperado
            if not getattr(response, "choices", None):
                raise ValueError(f"El modelo no devolvió una respuesta válida (choices es nulo).")
                
            message = response.choices[0].message
            
            # 2. Verificar llamadas a herramientas
            if hasattr(message, "tool_calls") and message.tool_calls:
                messages.append(cast(Any, message.model_dump(exclude_none=True)))

                for tool_call in message.tool_calls:
                    if tool_call.type != "function":
                        continue

                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                    resultado = {}

                    # Mapeo a Python tools
                    if func_name == "get_network_summary":
                        resultado = get_network_summary(args.get("region"))
                    elif func_name == "get_access_points_overview":
                        resultado = get_access_points_overview()
                    elif func_name == "get_anomalous_access_points":
                        resultado = get_anomalous_access_points(args.get("threshold", 1.3), args.get("region"))
                    elif func_name == "get_top_incident_access_points":
                        resultado = get_top_incident_access_points(args.get("limit", 5), args.get("region"))
                    elif func_name == "get_strategic_recommendations":
                        resultado = get_strategic_recommendations(args.get("region"))
                    elif func_name == "classify_failure_type":
                        resultado = classify_failure_type(args.get("ap_name"))
                    elif func_name == "generate_work_order":
                        resultado = generate_work_order(
                            ap_name=args.get("ap_name", "Desconocido"),
                            issue_type=args.get("issue_type", "Incidente general"),
                            priority=args.get("priority", "alta"),
                            reason=args.get("reason", "Afectación comunitaria crítica"),
                            region=args.get("region", "Desconocida")
                        )
                    else:
                        resultado = {"error": "Función no encontrada"}

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(resultado, ensure_ascii=False)
                    })

                # 3. Segunda llamada (respuesta final) con fallback
                final_response = self._call_with_fallback(messages)
                return final_response.choices[0].message.content or ""

            return message.content or ""

        except Exception as e:
            return f"Error en el servicio de IA (todos los modelos fallaron): {str(e)}"
