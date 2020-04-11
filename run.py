import os

from app import config_app

app = config_app()
app.secret_key = os.urandom(40)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
