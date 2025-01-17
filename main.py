from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

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
    "https://www.merkahorro.com",
    "https://backendpythonbot.vercel.app"
]

# Forzar HTTPS (Recomendado en producción)
app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes (puedes limitarlo en producción)
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Métodos específicos
    allow_headers=["*"],  # Todos los headers permitidos
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
            return {"response": "🤔 Lo siento, no pude entender tu pregunta. Sin embargo, puedo compartir información general sobre la empresa que podría ser útil: Merkahorro es una empresa en crecimiento con planes de expandirse a 12 ubicaciones en toda Colombia para 2026. Nos enfocamos en brindar productos y servicios de alta calidad en nuestros supermercados, con un compromiso con la satisfacción del cliente y el bienestar de los empleados."}

        intent = data['intents'][0]['name']

        responses = {
            'get_hours': """
            <h3>🕒 <strong>Horarios de nuestras sedes:</strong></h3>

            <div><strong>Copacabana Plaza:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Viernes:</strong> 7:00 AM - 8:00 PM</li>
                <li>🌅 <strong>Sábados:</strong> 6:30 AM - 8:00 PM</li>
                <li>🌙 <strong>Domingos:</strong> 7:00 AM - 5:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 7:00 AM - 4:00 PM</li>
            </ul>

            <div><strong>Copacabana Las Vegas:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Sábado:</strong> 7:30 AM - 8:30 PM</li>
                <li>🌙 <strong>Domingos:</strong> 7:30 AM - 3:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 7:30 AM - 3:00 PM</li>
            </ul>

            <div><strong>Copacabana San Juan:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Sábado:</strong> 7:30 AM - 8:30 PM</li>
                <li>🌙 <strong>Domingos:</strong> 7:30 AM - 3:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 7:30 AM - 3:00 PM</li>
            </ul>

            <div><strong>Girardota Parque:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Sábado:</strong> 7:00 AM - 8:00 PM</li>
                <li>🌙 <strong>Domingos:</strong> 7:00 AM - 4:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 8:00 AM - 3:00 PM</li>
            </ul>

            <div><strong>Girardota Llano:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Sábado:</strong> 7:00 AM - 8:00 PM</li>
                <li>🌙 <strong>Domingos:</strong> 7:00 AM - 4:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 8:00 AM - 3:00 PM</li>
            </ul>

            <div><strong>Barbosa:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Sábado:</strong> 7:00 AM - 8:00 PM</li>
                <li>🌙 <strong>Domingos:</strong> 7:00 AM - 4:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 7:00 AM - 4:00 PM</li>
            </ul>

            <div><strong>Villa Hermosa:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Sábado:</strong> 8:00 AM - 9:00 PM</li>
                <li>🌙 <strong>Domingos:</strong> 8:00 AM - 3:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 8:00 AM - 3:00 PM</li>
            </ul>

            <div><strong>Carnes Barbosa:</strong></div>
            <ul>
                <li>🌞 <strong>Lunes a Sábado:</strong> 7:00 AM - 8:00 PM</li>
                <li>🌙 <strong>Domingos:</strong> 7:00 AM - 4:00 PM</li>
                <li>🎉 <strong>Festivos:</strong> 8:00 AM - 4:00 PM</li>
            </ul>
            """,
            'get_locations': "📍 Contamos con 8 sedes. Si deseas obtener más información sobre cada una de ellas, como la ubicación exacta y el contacto por WhatsApp, te invitamos a visitar nuestra página principal. Allí podrás ver todos los detalles para cada sede.",
            'saludo': "👋 ¡Hola! ¿En qué puedo ayudarte hoy?",
            'trabaja_con_nosotros': "💼 Para postularte, mira las vacantes que hay disponibles, luego llena un formulario con tus datos y envíanos tu hoja de vida ¡Buena suerte!: https://www.merkahorro.com/trabaja-con-nosotros",
            'goodbye': "👋 ¡Hasta luego! ¡Que tengas un excelente día!",
            'promotions': "🎉 ¡Tenemos varias promociones increíbles! Para más detalles, visita nuestra página de promociones: https://www.merkahorro.com/promociones",
            'reservas': """
            📅 Si deseas hacer una reserva, sigue estos pasos:

            <ul>
                <li>🔑 Inicia sesión con tu correo en la sección de Login.</li>
                <li>🏛️ Selecciona un salón disponible de los dos que ofrecemos.</li>
                <li>📅 Haz clic en el botón flotante para ver el calendario con las reservas disponibles.</li>
                <li>📝 Haz clic en 'Reservar Aquí' para elegir la fecha y llenar el formulario con tus datos.</li>
                <li>✅ Completa la reserva y ¡listo!</li>
            </ul>

            Si necesitas cancelar tu reserva, sigue estos pasos:
            
            <ul>
                <li>❌ Selecciona la reserva que deseas cancelar.</li>
                <li>🗑️ Haz clic en 'Cancelar'.</li>
                <li>✍️ Completa los datos y confirma la cancelación.</li>
            </ul>

            ¡Es fácil y rápido!
            """,
             'developers': """
    🛠️ <strong>Desarrollado por:</strong>
    <ul>
        <li>👨‍💻 Johan Sanchez</li>
        <li>👨‍💻 Kevin Pineda</li>
        <li>👨‍💻 Juan Manuel Isaza</li>
    </ul>
    """,
            'contact_info': "📧 Contáctanos en paginaweb@merkahorrosas.com o al 📞 324 5597862.",

'get_social_media': """
<p>🌐 <strong>Puedes seguirnos en nuestras redes sociales</strong> para estar al tanto de todas nuestras novedades y promociones:</p>

<ul>
    <li>📸 <strong>Instagram</strong>: <a href="https://www.instagram.com/supermercadomerkahorro/?hl=es" target="_blank">@merkahorro</a></li>
    <li>👍 <strong>Facebook</strong>: <a href="https://www.facebook.com/supermercadosmerkahorro/?locale=es_LA" target="_blank">Merkahorro</a></li>
    <li>🎵 <strong>TikTok</strong>: <a href="https://www.tiktok.com/@supermercadomerkahorro" target="_blank">@merkahorro</a></li>
</ul>

<p>¡Síguenos y mantente informado sobre nuestras promociones, nuevos productos y mucho más! 🎉</p>
"""

        }

        return {"response": responses.get(intent, "🤔 Lo siento, no pude entender tu pregunta. ")}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectarse con Wit.ai: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {str(e)}")
