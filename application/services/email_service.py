import json

from flask_mail import Message

from application.decorators.decorators import async_task
from application.services.email import mail


@async_task
def send_async_email(msg):
    from run import app
    with app.app_context():
        mail.send(msg)


class EmailService:
    @classmethod
    def send_email(cls, email, password):
        msg = Message(subject="Recuperación de Clave",
                      sender='emprendebynicole@gmail.com',
                      recipients=[email],
                      body="Su clave temporal de accesso a Emprende by Nicole es: " + password)
        send_async_email(msg)

    @classmethod
    def send_confirmation_email(cls, email, body):
        body = body
        msg = Message(subject="Compra Confirmada. Emprende by Nicole",
                      sender='emprendebynicole@gmail.com',
                      recipients=[email],
                      body=body
                      )
        send_async_email(msg)
