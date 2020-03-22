from flask_mail import Message

from app import mail


class EmailService:
    @classmethod
    def send_email(cls, email, password):
        msg = Message(subject="Hello",
                      sender='emprendebynicole@gmail.com',
                      recipients=["jorgerodriguezchala@hotmail.com"],
                      body="Su clave temporal de accesso a Emprende by Nicole es: " + password)
        from run import app
        app.logger.debug('!!!!!!!!!!!!!')
        app.logger.debug(mail.state)
        mail.send(msg)
