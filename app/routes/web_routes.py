import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.services.llm_service import ask_agent

router = APIRouter()

# Ruta absoluta a templates para evitar problemas por directorio de ejecución.
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../app
templates_dir = os.path.join(base_dir, "templates")                    # .../app/templates
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    # TemplateResponse requiere pasar request en el contexto [web:13].
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/api/agent")
def agent_endpoint(prompt: str = Form(...)):
    """
    Endpoint API (sync a propósito):
    - La llamada al LLM (SDK) es bloqueante/síncrona.
    - Si lo dejas como async, puedes bloquear el event loop y "colgar" el server.
    """
    try:
        ai_text = ask_agent(prompt)
        return {
            "developer": settings.developer_name,
            "prompt": prompt,
            "answer": f"{settings.developer_name}: {ai_text}",
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
