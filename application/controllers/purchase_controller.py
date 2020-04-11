# https://codepen.io/robinhuy/pen/qjLxRq

from flask import Blueprint, request, session, render_template
from marshmallow import ValidationError

from application.controllers.dtos.purchase_dto import PurchaseDto
from application.models.purchase import Purchase
from application.services.order_service import OrderService
from application.services.purchase_service import PurchaseService

purchase_blueprint = Blueprint('/add_to_cart', __name__)
purchase_list_blueprint = Blueprint('/my_cart', __name__)
purchase_delete_blueprint = Blueprint('/delete', __name__)
purchase_confirm_blueprint = Blueprint('/confirm', __name__)


@purchase_blueprint.route('/add_to_cart', methods=['POST'])
def add_product_to_cart():
    try:
        data = request.get_json()
        purchase_service = PurchaseService()
        purchase_service.create_purchase(session['user_id'], data['id'],
                                         data['totalPrice'], data['units'], data['color'],
                                         data['size'], data['title'])
        return 'OK', 201
    except Exception as error:
        from run import app
        app.logger.debug(error)
        return 'Error saving data', 500


@purchase_list_blueprint.route('/my_cart', methods=['GET'])
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
    return dto


@purchase_delete_blueprint.route('/delete', methods=['PUT'])
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
def confirm_purchase():
    try:
        data = request.get_json()
        ids = data['ids']
        order_service = OrderService()
        order_id = order_service.save_order(ids[0], data['address'], data['city'], data['totalPrice'])
        purchase_service = PurchaseService()
        purchase_service.confirm_purchase(ids, order_id,)
        return 'OK', 201
    except Exception as error:
        from run import app
        app.logger.debug(error)
        return 'Error cancelando el producto', 500
