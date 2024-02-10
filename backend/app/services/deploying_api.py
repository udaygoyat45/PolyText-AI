from app import db, client
from openai import OpenAI
from celery import shared_task
import time


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run



@shared_task()
def understand_media(file_id):
    media = db.media_sources.find_one({'id': file_id}) 
    if 'scraped_text' not in media:
        return
    