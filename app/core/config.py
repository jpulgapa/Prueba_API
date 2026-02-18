import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Cargamos variables desde .env para no hardcodear secretos en el código.
load_dotenv()

@dataclass(frozen=True)
class Settings:
    """
    Config centralizada (buena práctica):
    - Facilita cambiar keys/modelos sin tocar código.
    - Evita duplicación y errores por nombres distintos.
    """
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    developer_name: str = os.getenv("DEVELOPER_NAME", "Desarrollador")
    model_name: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

settings = Settings()

def validate_settings() -> None:
    # Fallar rápido: si no hay key, no tiene sentido arrancar la app.
    if not settings.groq_api_key:
        raise RuntimeError("Falta GROQ_API_KEY en el entorno (.env).")
