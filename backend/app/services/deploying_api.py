from app import db, client, assistant
import os
from openai import OpenAI
from celery import shared_task
from celery.utils.log import get_task_logger
from moviepy.editor import VideoFileClip
import time

logger = get_task_logger(__name__)

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run



def mp3_to_text(mp3_location):
    transcript = client.audio.transcriptions.create(
        model='whisper-1',
        file=open(mp3_location, 'rb'),
        response_format='text'
    )

    return transcript




@shared_task()
def understand_media(file_id):
    logger.info("Understanding Media was called by Celery")
    media = db.media_sources.find_one({'id': file_id}) 

    if media['type'] == 'video/mp4':
        video = VideoFileClip(media['location'])
        audio_file_location = media['location'][:-4] + '.mp3'
        video.audio.write_audiofile(audio_file_location)
        audio_text = mp3_to_text(audio_file_location)
        text_file_location = os.path.join('data', 'media', 'temp.txt')
        with open(text_file_location, "w+") as fout:
            fout.write(audio_text)
        
        file = client.files.create(
            file=open(text_file_location, 'rb'),
            purpose = 'assistants'
        )
    
    elif media['type'] == 'audio/mpeg':
        audio_text = mp3_to_text(media['location'])
        text_file_location = os.path.join('data', 'media', 'temp.txt')
        with open(text_file_location, "w+") as fout:
            fout.write(audio_text)
        
        file = client.files.create(
            file=open(text_file_location, 'rb'),
            purpose = 'assistants'
        )
    
    elif media['type'] == 'image/jpeg':
        pass
    
    elif media['type'] == 'image/png':
        pass

    else:
        file = client.files.create(
            file=open(media['location'], 'rb'),
            purpose = 'assistants'
        ) 

    client.beta.assistants.files.create(assistant_id=assistant.id, file_id=file.id)