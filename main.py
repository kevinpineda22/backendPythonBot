from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear instancia de la aplicación FastAPI
app = FastAPI()

# Habilitar CORS para permitir solicitudes desde React
origins = [
    "http://localhost:3000",  # Si React corre en este puerto
    "http://127.0.0.1:3000",  # También para localhost si es diferente
    "http://localhost:5176",  # Puerto donde está corriendo React (Vite, por defecto)
    "http://127.0.0.1:5176",  # También para localhost si es diferente
    "https://construahorrosas.com"  # Dominio de tu página en SiteGround
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes de estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Token de acceso a Wit.ai desde las variables de entorno
access_token = os.getenv('WIT_ACCESS_TOKEN')

# Definición del modelo de mensaje
class Message(BaseModel):
    message: str

@app.post("/ask")
def ask(message: Message):
    # Llamar a Wit.ai con el mensaje del usuario
    url = f'https://api.wit.ai/message?v=20220101&q={message.message}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        intent = data['intents'][0]['name'] if data['intents'] else 'unknown'
        
        # Respuesta personalizada según la intención detectada
        if intent == 'get_hours':
            return {"response": "Estamos abiertos de lunes a sábado de 8:00 AM a 8:00 PM."}
        
        elif intent == 'get_locations':
            return {"response": "Contamos con 8 sedes. Para más información visita nuestra página principal."}
        
        elif intent == 'saludo':
            return {"response": "¡Hola! ¿En qué puedo ayudarte hoy?"}
        
        elif intent == 'trabaja_con_nosotros':
            return {"response": "Para postularte, visita: https://construahorrosas.com/trabaja-con-nosotros"}
        
        elif intent == 'goodbye':
            return {"response": "¡Hasta luego! ¡Que tengas un excelente día!"}
        
        elif intent == 'promotions':
            return {"response": "Consulta nuestras promociones aquí: https://construahorrosas.com/promociones"}
        
        elif intent == 'reservas':
            return {"response": "Inicia sesión y sigue los pasos para realizar una reserva."}
        
        elif intent == 'developers':
            return {"response": "Desarrollado por Kevin Pineda, Juan Isaza y Johan Sanchez."}
        
        elif intent == 'contact_info':
            return {"response": "Contáctanos en paginaweb@merkahorrosas.com o al 324 5597862."}
        
        else:
            return {"response": "Lo siento, no pude entender tu pregunta. Visita nuestra web para más información."}
    else:
        return {"response": "Lo siento, no pude procesar tu solicitud."}
