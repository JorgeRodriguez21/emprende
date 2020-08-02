# https://codepen.io/robinhuy/pen/qjLxRq
import json

from flask import Blueprint, request, session, render_template
from marshmallow import ValidationError

from application.controllers.dtos.purchase_dto import PurchaseDto
from application.middleware.is_user_logged import check_logged
from application.models.purchase import Purchase
from application.services.email_service import EmailService
from application.services.order_service import OrderService
from application.services.product_service import ProductService
from application.services.purchase_service import PurchaseService

purchase_blueprint = Blueprint('/add_to_cart', __name__)
purchase_list_blueprint = Blueprint('/my_cart', __name__)
purchase_delete_blueprint = Blueprint('/delete', __name__)
purchase_confirm_blueprint = Blueprint('/confirm', __name__)

product_service = ProductService()


@purchase_blueprint.route('/add_to_cart', methods=['POST'])
@check_logged
def add_product_to_cart():
    try:
        data = request.get_json()
        purchase_service = PurchaseService()
        if session.get('user_id') is None:
            return 'Debes iniciar sesion para realizar esta accion', 500
        purchase_service.create_purchase(session.get('user_id'), data['id'],
                                         data['totalPrice'], data['units'], data['color'],
                                         data['size'], data['title'], data['image'], data['option_selected'])
        return 'OK', 201
    except Exception as error:
        from run import app
        app.logger.error(error)
        return 'Error al guardar la compra', 500


@purchase_list_blueprint.route('/my_cart', methods=['GET'])
@check_logged
def get_active_purchases():
    try:
        purchase_service = PurchaseService()

        if session['user_id'] is None:
            raise Exception("No ha iniciado sesión")
        purchases = purchase_service.get_active_purchases_for_active_user(session['user_id'])
        dtos = map(map_to_purchase_dto, purchases)
        dto_list = list(dtos)
        response = []
        for dto in dto_list:
            response.append(dto.__dict__)
        summary = purchase_service.get_last_summary(session['user_id'])
        return render_template('shopping_cart.html', purchases=response, summary=summary)
    except Exception as error:
        from run import app
        app.logger.debug(error)
        raise ValidationError("Error cargando las compras")


def map_to_purchase_dto(purchase: Purchase):
    dto = PurchaseDto()
    product = product_service.find_product_by_id(purchase.product_id)
    dto.id = purchase.id
    dto.user_id = purchase.user_id
    dto.product_id = purchase.product_id
    dto.units = purchase.units
    dto.price = purchase.price
    dto.status = purchase.status
    dto.title = purchase.features['title']
    dto.color = purchase.features['color']
    dto.size = purchase.features['size']
    dto.image = purchase.features['image']
    dto.sale_price = product.sale_price * purchase.units
    return dto


@purchase_delete_blueprint.route('/delete', methods=['PUT'])
@check_logged
def delete_product_from_cart():
    try:
        data = request.get_json()
        purchase_service = PurchaseService()
        purchase_service.cancel_purchase(data['id'])
        return 'OK', 201
    except Exception as error:
        from run import app
        app.logger.debug(error)
        return 'Error cancelando el producto', 500


@purchase_confirm_blueprint.route('/confirm', methods=['PUT'])
@check_logged
def confirm_purchase():
    from run import app
    try:
        data = request.get_json()
        ids = data['ids']
        purchase_service = PurchaseService()
        purchase_service.check_products_availability(ids)
        order_service = OrderService()
        order = order_service.save_order(ids[0], data['address'], data['city'], data['totalPrice'])
        purchases = purchase_service.confirm_purchase(ids, order.id)
        summary = create_summary(purchases, order.code, order.total_price, app.config['CONTACT_PHONE'])
        user_info = get_user_name(purchases[0].user) + " " + purchases[0].user.phone
        order_service.save_user_info(order.id, user_info)
        purchase_service.update_summary(ids, summary)
        email_service = EmailService()
        email_service.send_confirmation_email(session['user_email'], summary)
        return 'OK', 201
    except ValidationError as error:
        app.logger.error(error)
        return error.messages[0], 500
    except Exception as error:
        app.logger.error(error)
        return 'Error confirmando la compra', 500


def get_user_name(user):
    return user.name + " " + user.last_name


def create_summary(purchases, code, price, phone):
    product_details = ''
    for purchase in purchases:
        product_details = product_details + ' \n ' + purchase.features['title'] + ' : ' + str(
            purchase.units) + ' unidad(es).'
    message = "Hola" + " " + get_user_name(purchases[
                                               0].user) + "\n" + "El código de su compra es: " + code + " . Los productos que usted adquirió son los siguientes: " + \
              product_details + "\n" + "El precio total es de $" + str(
        price) + ". Por favor comunicarse por whatsapp con el número " + phone + \
              " para coordinar el pago y la entrega.\n El pago debe hacerse dentro de las próximas 2 horas o su pedido será cancelado. \n" \
              "Gracias por confiar en nosotros."
    return message
