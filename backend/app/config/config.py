import os

class Config:
    def __init__(self):
        self.dev_config = DevelopmentConfig()

class DevelopmentConfig():
    ENV = "development"
    HOST = "0.0.0.0"
    DEBUG = True
    PORT = 4000
    MONGODB_DATABASE_URI = 'mongodb://localhost:27017'
    UPLOAD_FOLDER = './data/media/'
    REDIS_DATABASE_URI = 'redis://localhost'
    CELERY = dict(
        broker_url="redis://127.0.0.1:6379",
        result_backend="redis://127.0.0.1:6379",
        broker_connection_retry_on_startup=True
    )