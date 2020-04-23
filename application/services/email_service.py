import json

from flask_mail import Message

from application.services.email import mail


class EmailService:
    @classmethod
    def send_email(cls, email, password):
        msg = Message(subject="Recuperación de Clave",
                      sender='emprendebynicole@gmail.com',
                      recipients=[email],
                      body="Su clave temporal de accesso a Emprende by Nicole es: " + password)
        mail.send(msg)

    @classmethod
    def send_confirmation_email(cls, email, code, purchases, price, phone):
        product_details = ''
        for purchase in purchases:
            product_details = product_details + ' \n ' + purchase.features['title'] + ' : ' + str(
                purchase.units) + ' unidad(es).'
        body = "El código de su compra es: " + code + " . Los productos que usted adqurió son los siguientes: " + \
               product_details + "\n" + "El precio total es de $" + str(
            price) + ". Por favor comunicarse por whatsapp con el número " + phone + \
               " para coordinar el pago y la entrega.\n Gracias por confiar en nosotros."

        msg = Message(subject="Compra Confirmada. Emprende by Nicole",
                      sender='emprendebynicole@gmail.com',
                      recipients=[email],
                      body=body
                      )
        mail.send(msg)
