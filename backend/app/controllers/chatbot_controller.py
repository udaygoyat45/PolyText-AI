from flask import Blueprint, jsonify, request, Response
from celery import chain
from app import db, client
chatbot = Blueprint("chatbot", __name__)


@chatbot.route("ping")
def ping_test():
    return "API connection working"


@chatbot.route("list")
def list_threads():
    threads = list(db.openai_threads.find())
    threads_id = [thread['id'] for thread in threads]
    return {'threads': threads_id}
    

@chatbot.route("create_thread")
def create_thread():
    thread = client.beta.threads.create()
    meta_thread = {
        'id': thread.id,
        'created_at': thread.created_at,
    }

    print("DEBUG")
    print(thread)
    db.openai_threads.insert_one(meta_thread)
    return {'thread': thread.id}