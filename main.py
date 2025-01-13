
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI()

# Token de acceso a Wit.ai desde .env
access_token = os.getenv('WIT_ACCESS_TOKEN')
if not access_token:
    raise ValueError("❌ El TOKEN de Wit.ai no está definido en el archivo .env.")

# Configuración de CORS mejorada
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5176",
    "http://127.0.0.1:5176",
    "https://construahorrosas.com",
    "https://backendpythonbot.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta para el favicon
@app.get("/icono.ico")
async def favicon():
    return FileResponse("static/icono.ico")

# Modelo de mensaje
class Message(BaseModel):
    message: str

# Ruta para validar el servidor
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
        response.raise_for_status()
        data = response.json()

        if not data.get('intents'):
            return {"response": "🤔 No pude entender tu pregunta. Visita nuestra web para más información."}

        intent = data['intents'][0]['name']

        responses = {
            'get_hours': "🕒 Estamos abiertos de lunes a sábado de 8:00 AM a 8:00 PM.",
            'get_locations': "📍 Contamos con 8 sedes. Visita nuestra página principal.",
            'saludo': "👋 ¡Hola! ¿En qué puedo ayudarte hoy?",
            'trabaja_con_nosotros': "💼 Para postularte, visita: https://construahorrosas.com/trabaja-con-nosotros",
            'goodbye': "👋 ¡Hasta luego! ¡Que tengas un excelente día!",
            'promotions': "🎉 Consulta nuestras promociones: https://construahorrosas.com/promociones",
            'reservas': "📅 Inicia sesión y sigue los pasos para realizar una reserva.",
            'developers': "🛠️ Desarrollado por Kevin Pineda, Juan Isaza y Johan Sanchez.",
            'contact_info': "📧 Contáctanos en paginaweb@merkahorrosas.com o al 📞 324 5597862."
        }

        return {"response": responses.get(intent, "🤔 Lo siento, no pude entender tu solicitud. Visita nuestra web para más información.")}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectarse con Wit.ai: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {str(e)}")

