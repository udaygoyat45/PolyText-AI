from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from app.config.config import Config
from pymongo import MongoClient
from openai import OpenAI
from .utils import celery_init_app

app = Flask(__name__)
CORS(app)

config = Config().dev_config
app.env = config.ENV

db = MongoClient(config.MONGODB_DATABASE_URI).polytext
socketio = SocketIO(app,
                    cors_allowed_origins="*",
                    message_queue=config.REDIS_DATABASE_URI)

app.config["CELERY"] = config.CELERY
celery_app = celery_init_app(app)
celery_app.set_default()


client = OpenAI(api_key="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")



assistant_list = list(client.beta.assistants.list())

if len(assistant_list) > 0:
    assistant = client.beta.assistants.retrieve(assistant_list[0].id)
else:
    assistant = client.beta.assistants.create(
        name="PolyText AI",
        instructions="You are an expert in understanding any media file. When user asks a question, find the right file and answer the question accurately. Try to keep it short. ",
        model="gpt-4-1106-preview",
        tools = [{"type": 'retrieval'}]
    )


from app.controllers.socket_controller import *
from app.controllers.media_controller import media
from app.controllers.chatbot_controller import chatbot

app.register_blueprint(media, url_prefix="/media")
app.register_blueprint(chatbot, url_prefix="/chatbot")