import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.services.llm_service import ask_agent

router = APIRouter()


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_dir = os.path.join(base_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Ruta principal que renderiza la página HTML"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/api/agent")
def agent_endpoint(prompt: str = Form(...)):
    """Endpoint API para procesar peticiones al agente IA."""
    try:
        ai_text = ask_agent(prompt)
        return {
            "developer": settings.developer_name,
            "prompt": prompt,
            "answer": f"{settings.developer_name}: {ai_text}",
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
