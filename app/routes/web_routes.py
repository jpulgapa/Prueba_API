# Importación de módulos necesarios para las rutas web
import os  # Para manipular rutas de archivos
from fastapi import APIRouter, Request, Form  # APIRouter para definir rutas, Request para peticiones, Form para datos de formulario
from fastapi.responses import HTMLResponse, JSONResponse  # Tipos de respuesta HTTP
from fastapi.templating import Jinja2Templates  # Motor de plantillas HTML

from app.core.config import settings  # Configuración de la aplicación (API key, nombre, modelo)
from app.services.llm_service import ask_agent  # Servicio para comunicarse con el LLM de Groq

# Crear router para agrupar las rutas de esta aplicación
router = APIRouter()


# Configurar directorio de plantillas HTML usando ruta absoluta
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Obtener directorio app/
templates_dir = os.path.join(base_dir, "templates")  # Ruta absoluta a app/templates
templates = Jinja2Templates(directory=templates_dir)  # Inicializar motor de plantillas Jinja2

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Ruta principal que renderiza la página HTML del chat."""
    # Devolver la plantilla index.html con el contexto de la petición
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/api/agent")
def agent_endpoint(prompt: str = Form(...)):
    """
    Endpoint API para procesar peticiones al agente IA.
    
    Recibe:
    - prompt: Texto enviado por el usuario desde el formulario HTML
    
    Devuelve:
    - JSON con el nombre del desarrollador, el prompt y la respuesta del agente
    
    Nota: Esta función es síncrona porque el SDK de OpenAI/Groq hace llamadas bloqueantes.
    Usar async aquí bloquearía el event loop de FastAPI.
    """
    try:
        # Llamar al servicio LLM para obtener respuesta del agente
        ai_text = ask_agent(prompt)
        # Devolver respuesta en formato JSON
        return {
            "developer": settings.developer_name,  # Nombre del desarrollador desde .env
            "prompt": prompt,  # Prompt recibido
            "answer": f"{settings.developer_name}: {ai_text}",  # Respuesta formateada
        }
    except Exception as e:
        # En caso de error, devolver JSON con mensaje de error y código 500
        return JSONResponse({"error": str(e)}, status_code=500)
