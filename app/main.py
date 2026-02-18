import os
import time
import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.core.config import validate_settings
from app.routes.web_routes import router as web_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

def create_app() -> FastAPI:
    validate_settings()

    app = FastAPI(title="Prueba Agente API", version="1.0.0")

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        ms = int((time.time() - start) * 1000)
        logger.info("%s %s -> %s (%sms)", request.method, request.url.path, response.status_code, ms)
        return response

    
    base_dir = os.path.dirname(os.path.abspath(__file__))   
    static_dir = os.path.join(base_dir, "static")      
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    app.include_router(web_router)
    return app

app = create_app()
