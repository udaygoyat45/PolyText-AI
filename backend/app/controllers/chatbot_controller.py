from flask import Blueprint, jsonify, request, Response
from celery import chain
from app import db, client
chatbot = Blueprint("chatbot", __name__)


@chatbot.route("ping")
def ping_test():
    return "API connection working"


@chatbot.route("list")
def list_threads():
    j