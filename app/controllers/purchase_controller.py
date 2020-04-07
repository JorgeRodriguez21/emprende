# https://codepen.io/robinhuy/pen/qjLxRq
from flask import Blueprint, request, session, render_template
from marshmallow import ValidationError

from app.controllers.dtos.purchase_dto import PurchaseDto
from app.models.purchase import Purchase
from app.services.purchase_service import PurchaseService

purchase_blueprint = Blueprint('/add_to_cart', __name__)
purchase_list_blueprint = Blueprint('/my_cart', __name__)


@purchase_blueprint.route('/add_to_cart', methods=['POST'])
def add_product_to_cart():
    try:
        data = request.get_json()
        purchase_service = PurchaseService()
        from run import app
        purchase_service.create_purchase(session['user_id'], data['id'],
                                         data['totalPrice'], data['units'], data['color'],
                                         data['size'], data['title'])
        return 'OK'
    except Exception as error:
        from run import app
        app.logger.debug(error)
        raise ValidationError("Error saving data")


@purchase_list_blueprint.route('/my_cart', methods=['GET'])
def get_active_purchases():
    from run import app
    try:
        purchase_service = PurchaseService()
        purchases = purchase_service.get_active_purchases_for_active_user(session['user_id'])
        dtos = map(map_to_purchase_dto, purchases)
        app.logger.debug(dtos)
        return render_template('shopping_cart.html', purchases=set(dtos))
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
    dto.purchase_code = purchase.purchase_code
    dto.title = purchase.features['title']
    dto.color = purchase.features['color']
    dto.size = purchase.features['size']
    return dto
