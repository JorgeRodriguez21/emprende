# https://codepen.io/robinhuy/pen/qjLxRq

from flask import Blueprint, request, session, render_template
from marshmallow import ValidationError

from application.controllers.dtos.purchase_dto import PurchaseDto
from application.middleware.is_user_logged import check_logged
from application.models.purchase import Purchase
from application.services.email_service import EmailService
from application.services.order_service import OrderService
from application.services.purchase_service import PurchaseService

purchase_blueprint = Blueprint('/add_to_cart', __name__)
purchase_list_blueprint = Blueprint('/my_cart', __name__)
purchase_delete_blueprint = Blueprint('/delete', __name__)
purchase_confirm_blueprint = Blueprint('/confirm', __name__)


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
                                         data['size'], data['title'], data['image'])
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
        purchases = purchase_service.get_active_purchases_for_active_user(session['user_id'])
        dtos = map(map_to_purchase_dto, purchases)
        dto_list = list(dtos)
        response = []
        for dto in dto_list:
            response.append(dto.__dict__)
        return render_template('shopping_cart.html', purchases=response)
    except Exception as error:
        from run import app
        app.logger.debug(error)
        raise ValidationError("Error loading purchases")


def map_to_purchase_dto(purchase: Purchase):
    dto = PurchaseDto()
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
        order_service = OrderService()
        order = order_service.save_order(ids[0], data['address'], data['city'], data['totalPrice'])
        purchase_service = PurchaseService()
        purchases = purchase_service.confirm_purchase(ids, order.id)
        email_service = EmailService()
        email_service.send_confirmation_email(session['user_email'], order.code, purchases, order.total_price,
                                              app.config['CONTACT_PHONE'])
        return 'OK', 201
    except Exception as error:
        app.logger.error(error)
        return 'Error confirmando la compra', 500
