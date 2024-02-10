from flask import Blueprint, jsonify, request, Response
from app.services import deploying_api
from celery import chain
from app import db, client, assistant
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
        'messages': []
    }

    print("DEBUG")
    print(thread)
    db.openai_threads.insert_one(meta_thread)
    return {'thread': thread.id}


@chatbot.route("list_messages/<thread_id>")
def list_messages(thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    reversed_messages = reversed(messages.data)
    parsed_messages = [{'role': a.role, 'content': a.content[0].text.value} for a in reversed_messages]
    return {'messages': parsed_messages}

    
@chatbot.route("new_message/<thread_id>/<query>")
def new_message(thread_id, query):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role = 'user',
        content = query
    )

    messages_now = db.openai_threads.find_one({'id': thread_id})['messages']
    messages_now.append({'role': 'user', 'content': query})

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant.id
    )

    thread = client.beta.threads.retrieve(thread_id)
    ai_reply = deploying_api.wait_on_run(run, thread)

    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    new_message = messages.data[0]
    messages_now.append({'role': new_message.role, 'content': new_message.content[0].text.value})

    db.openai_threads.update_one({'id': thread_id}, {'$set': {'messages': messages_now}})

    return {
        'reply': new_message.content[0].text.value
    }