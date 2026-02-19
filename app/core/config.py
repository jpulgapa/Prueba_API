import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:

    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    developer_name: str = os.getenv("DEVELOPER_NAME", "Desarrollador")
    model_name: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

settings = Settings()

def validate_settings() -> None:
    
    if not settings.groq_api_key:
        raise RuntimeError("Falta GROQ_API_KEY en el entorno (.env).")
