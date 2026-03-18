from app import app

# gunicorn ищет переменную 'application'
application = app.server

if __name__ == "__main__":
    application.run()