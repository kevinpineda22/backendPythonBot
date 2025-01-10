from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

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

# Token de acceso a Wit.ai
access_token = 'GWNEP7ZPR2LL4GPI2XH5ZRD3VZF4QAX4'  # Reemplaza con tu token de acceso

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
        if intent == 'get_hours':  # Si la intención es 'get_hours'
            return {"response": "Estamos abiertos de lunes a sábado de 8:00 AM a 8:00 PM."}
        
        elif intent == 'get_locations':  # Si la intención es 'get_locations'
            return {"response": "Contamos con 8 sedes. Si deseas obtener más información sobre cada una de ellas, como la ubicación exacta y el contacto por WhatsApp, te invitamos a visitar nuestra página principal. Allí podrás ver todos los detalles para cada sede."}
        
        elif intent == 'saludo':  # Si la intención es 'greeting'
            return {"response": "¡Hola! ¿En qué puedo ayudarte hoy?"}

        elif intent == 'trabaja_con_nosotros':  # Si la intención es 'how_to_apply'
            return {
                "response": "Para postularte, mira las vacantes que hay disponibles, luego llena un formulario con tus datos y envianos tu hoja de vida ¡Buena suerte!: https://construahorrosas.com/trabaja-con-nosotros"
            }

        elif intent == 'goodbye':  # Si la intención es 'goodbye'
            return {"response": "¡Hasta luego! ¡Que tengas un excelente día!"}
        
        elif intent == 'promotions':  # Si la intención es 'promotions'
            return {"response": "¡Tenemos varias promociones increíbles! Para más detalles, visita nuestra página de promociones: https://construahorrosas.com/promociones"}
        
        elif intent == 'reservas':  # Si la intención es 'reservas'
            return {"response": "1.Inicia sesión con tu correo en la sección de Login. 2.Selecciona un salón disponible de los dos que ofrecemos. 3.Haz clic en el botón flotante para ver el calendario con las reservas disponibles. 4.Haz clic en Reservar Aquí para elegir la fecha y llenar el formulario con tus datos. 5.Completa la reserva y ¡listo!... Si necesitas cancelar, selecciona la reserva y haz clic en Cancelar. Completa los datos y confirma la cancelación."}
        
        elif intent == 'developers':  # Nueva intención para saber quiénes son los desarrolladores
            return {
                "response": "Esta página fue creada y desarrollada por el equipo de desarrollo de Merkahorro. Kevin Pineda, Juan Isaza y Johan Sanchez"
            }
        
        # Nueva intención para manejar preguntas de contacto
        elif intent == 'contact_info':  # Si la intención es 'contact_info'
            return {
                "response": "Puedes contactarnos a través del correo electrónico en paginaweb@merkahorrosas.com o escribenos al 324 5597862."
            }
        
        else:
            return {"response": "Lo siento, no pude entender tu pregunta.Sin embargo, puedo compartir información general sobre la empresa que podría ser útil: Merkahorro es una empresa en crecimiento con planes de expandirse a 12 ubicaciones en toda Colombia para 2026. Nos enfocamos en brindar productos y servicios de alta calidad en nuestros supermercados, con un compromiso con la satisfacción del cliente y el bienestar de los empleados. "}
    else:
        return {"response": "Lo siento, no pude procesar tu solicitud."}