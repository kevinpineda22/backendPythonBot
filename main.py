from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI()

# Token de acceso a Wit.ai desde .env
access_token = os.getenv('WIT_ACCESS_TOKEN')
if not access_token:
    raise ValueError("❌ El TOKEN de Wit.ai no está definido en el archivo .env.")

# Agregar el origen correcto en la configuración de CORS
origins = [
    "http://localhost:3000",  # Si estás trabajando en local
    "http://127.0.0.1:3000",  # También para localhost si es diferente
    "http://localhost:5176",  # Si usas Vite para desarrollo en local
    "http://127.0.0.1:5176",  # Si usas Vite en localhost
    "https://construahorrosas.com",  # El dominio de tu frontend en producción
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta para el favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Modelo de mensaje
class Message(BaseModel):
    message: str

# Ruta principal para validar el servidor
@app.get("/")
def read_root():
    return {"message": "🚀 Backend del ChatBot de Merkahorro está funcionando correctamente."}

# Ruta para procesar los mensajes
@app.post("/ask")
def ask(message: Message):
    url = f'https://api.wit.ai/message?v=20220101&q={message.message}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Validar errores HTTP

        data = response.json()
        intent = data['intents'][0]['name'] if data['intents'] else 'unknown'

        # Respuestas personalizadas
        if intent == 'get_hours':
            return {"response": "🕒 Estamos abiertos de lunes a sábado de 8:00 AM a 8:00 PM."}
        elif intent == 'get_locations':
            return {"response": "📍 Contamos con 8 sedes. Visita nuestra página principal."}
        elif intent == 'saludo':
            return {"response": "👋 ¡Hola! ¿En qué puedo ayudarte hoy?"}
        elif intent == 'trabaja_con_nosotros':
            return {"response": "💼 Para postularte, visita: https://construahorrosas.com/trabaja-con-nosotros"}
        elif intent == 'goodbye':
            return {"response": "👋 ¡Hasta luego! ¡Que tengas un excelente día!"}
        elif intent == 'promotions':
            return {"response": "🎉 Consulta nuestras promociones: https://construahorrosas.com/promociones"}
        elif intent == 'reservas':
            return {"response": "📅 Inicia sesión y sigue los pasos para realizar una reserva."}
        elif intent == 'developers':
            return {"response": "🛠️ Desarrollado por Kevin Pineda, Juan Isaza y Johan Sanchez."}
        elif intent == 'contact_info':
            return {"response": "📧 Contáctanos en paginaweb@merkahorrosas.com o al 📞 324 5597862."}
        else:
            return {"response": "🤔 Lo siento, no pude entender tu pregunta. Visita nuestra web para más información."}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectarse con Wit.ai: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")
