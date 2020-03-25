from flask_mail import Message

from app.services.email import mail


class EmailService:
    @classmethod
    def send_email(cls, email, password):
        msg = Message(subject="Hello",
                      sender='emprendebynicole@gmail.com',
                      recipients=[email],
                      body="Su clave temporal de accesso a Emprende by Nicole es: " + password)
        mail.send(msg)
