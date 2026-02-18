# Módulo de configuración centralizada de la aplicación
import os  # Para leer variables de entorno
from dataclasses import dataclass  # Para crear clases de datos inmutables
from dotenv import load_dotenv  # Para cargar variables desde archivo .env

# Cargar variables de entorno desde el archivo .env en la raíz del proyecto
load_dotenv()

@dataclass(frozen=True)
class Settings:
    """
      Configuración centralizada de la aplicación.
    
    Buena práctica: mantener toda la configuración en un solo lugar
    facilita cambios y evita hardcodear valores sensibles en el código.
    """
    # Clave API de Groq obtenida del archivo .env
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    # Nombre del desarrollador que aparecerá en las respuestas
    developer_name: str = os.getenv("DEVELOPER_NAME", "Desarrollador")
    # Modelo de IA a utilizar (por defecto llama-3.3-70b-versatile)
    model_name: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# Crear instancia única de configuración (patrón Singleton)
settings = Settings()

def validate_settings() -> None:
    """
    Valida que existan las configuraciones críticas.
    
    Principio "fail fast": si falta la API key, es mejor fallar inmediatamente
    al iniciar la app que esperar a que haya errores durante su ejecución.
    """
    if not settings.groq_api_key:
        raise RuntimeError("Falta GROQ_API_KEY en el entorno (.env).")
