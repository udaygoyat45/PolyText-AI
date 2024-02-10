from flask import request, Response, json, Blueprint, jsonify
from werkzeug.utils import secure_filename
from celery import chain
from app.services import scraper
import bson
from app import config, db
import os

media = Blueprint("books", __name__)


@media.route("ping")
def ping_test():
    return "API connection working"


@media.route("check/<format>")
def check_format(format):
    supported_formats = [
        'application-pdf',
        'application-vnd.openxmlformats-officedocument.presentationml.presentation'
        'text-plain'
        ]

    format = format.lower()
    return {'media_supported': format in supported_formats}


@media.route("list")
def list_media():
    all_media = list(db.media_sources.find({}, {"_id": 0, 'name': 1, 'type': 1}))
    return {'medias': all_media}


@media.route('upload', methods=['GET', 'POST'])
def upload_media():
    if request.method == 'POST':
        if 'file' not in request.files:
            return {'error': "No file detected"}

        file = request.files['file']
        if file.filename == '':
            return {'error': "No file detected"}
        
        if file:
            filename = secure_filename(file.filename)
            file_type = file.headers['Content-Type'] 
            file_location = os.path.join(config.UPLOAD_FOLDER, filename)

            file.save(file_location)

            new_media = {
                'id': str(bson.objectid.ObjectId()),
                'name': filename,
                'type': file_type,
                'location': file_location,
                'scraped': False,
                'ai_deploy': False
            }

            db.media_sources.insert_one(new_media.copy())

            # call celery task to start scraping the file here
            
            chain(
                scraper.scrape.delay.s(new_media['id']),
                
            ).apply_async()

            return {'success': "File upload successful", 'new_media': new_media}



@media.route("text/<text_link>")
def get_book(book_id):
    return "TODO: work with text"


@media.route("pdf/<pdf_link>")
def list_books(pdf_link):
    return "TODO: work with pdfs"