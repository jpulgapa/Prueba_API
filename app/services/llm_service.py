# Servicio para interactuar con el modelo de lenguaje (LLM)
from openai import OpenAI  # Cliente de OpenAI compatible con Groq
from app.core.config import settings  # Importar configuración (API key, modelo)

# Groq ofrece una API compatible con OpenAI, solo necesitamos cambiar la URL base
# Esto permite usar el SDK de OpenAI para conectarse a Groq

# Crear cliente de OpenAI configurado para usar Groq
client = OpenAI(
    api_key=settings.groq_api_key,  # API key de Groq desde el archivo .env
    base_url="https://api.groq.com/openai/v1",  # URL específica de Groq para compatibilidad OpenAI
)

def ask_agent(prompt: str) -> str:
    """
    Envía un prompt al agente IA y devuelve su respuesta.
    
    Args:
        prompt: Pregunta o instrucción del usuario
        
    Returns:
        Respuesta generada por el modelo de IA
        
    Buena práctica: Encapsular la lógica del LLM en una función permite
    cambiar de proveedor o modelo sin modificar las rutas/controladores.
    """
    # Limpiar espacios en blanco del prompt
    prompt = (prompt or "").strip()
    # Validar que el prompt no esté vacío
    if not prompt:
        return "Por favor envía un prompt no vacío."

    # Crear una conversación con el modelo usando la API de chat completions
    completion = client.chat.completions.create(
        model=settings.model_name,  # Modelo configurado en .env (ej: llama-3.3-70b-versatile)
        messages=[
            # Mensaje del sistema: define el comportamiento del asistente
            {"role": "system", "content": "Eres un asistente útil y conciso."},
            # Mensaje del usuario: el prompt enviado desde el frontend
            {"role": "user", "content": prompt},
        ],
        # Aquí podrías agregar parámetros como temperature, max_tokens, etc.
    )
    # Extraer y devolver el contenido de la primera respuesta
    return completion.choices[0].message.content or ""
