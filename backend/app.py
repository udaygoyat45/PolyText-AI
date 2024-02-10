from app import config, app, socketio, celery_app

if __name__ == "__main__":
    socketio.run(app,
                 host=config.HOST,
                 port=config.PORT,
                 debug=config.DEBUG
                )
