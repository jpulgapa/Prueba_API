# Importaciones necesarias para el servidor web
import os  # Para manejar rutas de archivos
import time  # Para medir tiempo de respuesta de peticiones
import logging  # Para registrar eventos y errores

from fastapi import FastAPI, Request  # Framework web y objeto de petición
from fastapi.staticfiles import StaticFiles  # Para servir archivos estáticos (CSS, JS, imágenes)

from app.core.config import validate_settings  # Valida que existan las variables de entorno necesarias
from app.routes.web_routes import router as web_router  # Importa las rutas de la aplicación

# Configuración del sistema de logging
logging.basicConfig(level=logging.INFO)  # Nivel INFO muestra mensajes informativos
logger = logging.getLogger("app")  # Crea un logger específico para la app

def create_app() -> FastAPI:
    """Función factory que crea y configura la aplicación FastAPI."""
    # Validar que existan las variables de entorno requeridas (GROQ_API_KEY)
    validate_settings()

    # Crear instancia de FastAPI con título y versión
    app = FastAPI(title="Prueba Agente API", version="1.0.0")

    # Middleware para registrar todas las peticiones HTTP
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()  # Momento de inicio de la petición
        response = await call_next(request)  # Procesar la petición
        ms = int((time.time() - start) * 1000)  # Calcular tiempo en milisegundos
        # Registrar método, ruta, código de respuesta y tiempo
        logger.info("%s %s -> %s (%sms)", request.method, request.url.path, response.status_code, ms)
        return response

    # Configurar directorio de archivos estáticos (CSS, imágenes)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual (app/)
    static_dir = os.path.join(base_dir, "static")  # Ruta a app/static
    # Montar carpeta static para que /static/styles.css sirva archivos CSS
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Registrar las rutas web (GET / y POST /api/agent)
    app.include_router(web_router)
    return app

# Crear la instancia de la aplicación (uvicorn buscará esta variable)
app = create_app()
