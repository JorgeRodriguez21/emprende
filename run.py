import os

from app import config_app

app = config_app()

if __name__ == '__main__':
    app.secret_key = os.urandom(40)
    app.run(host='0.0.0.0')
