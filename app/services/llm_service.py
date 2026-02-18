from openai import OpenAI
from app.core.config import settings

# Groq usa API OpenAI-compatible cambiando base_url a:
# https://api.groq.com/openai/v1 [web:64][web:150]
client = OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)

def ask_agent(prompt: str) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        return "Por favor envía un prompt no vacío."

    completion = client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {"role": "system", "content": "Eres un asistente útil y conciso."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content or ""
