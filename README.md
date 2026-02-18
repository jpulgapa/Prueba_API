# Prueba tecnica de Agente API (FastAPI + GroqCloud)

API en Python que actúa como intermediario entre un usuario y un modelo LLM (GroqCloud).
El usuario envía un `prompt` y la API responde con la respuesta del modelo incluyendo el nombre del desarrollador.
 Requisitos
- Python 3.10+ (recomendado 3.11+)
- Una API Key de GroqCloud

Groq es compatible con el cliente de OpenAI usando `base_url="https://api.groq.com/openai/v1"` [web:64].

---

## Estructura del proyecto
─ app/
 ─ main.py --- Punto de entrada de la aplicación
 ─ core/config.py ---    # Configuración y carga de variables de entorno
 ─ services/llm_service.py ---- Lógica de conexión con GroqCloud
 ─ routes/web_routes.py ---- Endpoints y renderizado HTML
 ─ templates/index.html ---- Interfaz
 ─ static/styles.css ---- Estilos
 ─ .env
 ─ README.md
 ─ requirements.txt

## Variables de entorno (.env)

Crea un archivo .env en la raíz y pegaras lo siguiente:

GROQ_API_KEY=" TU_KEY " (aca pondrias tu key generada desde https://console.groq.com/keys )
DEVELOPER_NAME= (Pones el nombre con el que quieres que te llame el agente)
MODEL_NAME=llama-3.3-70b-versatile

## Instalar dependencias y correr el proyecto 
Clona el repositorio y luego instala las dependencias 

- py -m pip install -r requirements.txt 
- Luego para ejecutarlo = uvicorn app.main:app --reload
