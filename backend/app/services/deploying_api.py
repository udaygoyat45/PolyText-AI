from app import db
from openai import OpenAI
from celery import shared_task


@shared_task()
def understand_media(file_id):
    media = db.media_sources.find_one({'id': file_id}) 
    if 'scraped_text' not in media:
        return
    