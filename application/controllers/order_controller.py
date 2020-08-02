from flask import Blueprint, render_template, request
from marshmallow import ValidationError

from application.controllers.dtos.purchase_dto import PurchaseDto
from application.middleware.is_user_logged import check_is_admin
from application.models.purchase import Purchase
from application.services.order_service import OrderService
from application.services.product_service import ProductService

orders_blueprint = Blueprint('/orders', __name__)
order_detail_blueprint = Blueprint('/order/<order_id>', __name__)
order_confirmation_blueprint = Blueprint('/order/confirmation', __name__)
order_cancellation_blueprint = Blueprint('/order/cancellation', __name__)

product_service = ProductService()


@orders_blueprint.route('/orders', methods=['GET'])
@check_is_admin
def get_all_pending_orders():
    try:
        order_service = OrderService()
        orders = order_service.get_all_pending_orders()
        return render_template('order_list.html', orders=orders)
    except Exception as error:
        from run import app
        app.logger.error(error)
        raise ValidationError("Error al cargar las ordenes")


@order_detail_blueprint.route('/order/<order_id>', methods=['GET'])
@check_is_admin
def get_order(order_id):
    try:
        order_service = OrderService()
        order = order_service.get_order_by_id(order_id)
        dtos = map(map_to_purchase_dto, order.purchases)
        dto_list = list(dtos)
        response = []
        for dto in dto_list:
            response.append(dto.__dict__)
        return render_template('order_detail.html', order=order, purchases=response)
    except Exception as error:
        from run import app
        app.logger.error(error)
        raise ValidationError("Error al cargar la orden")


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


@order_confirmation_blueprint.route('/order/confirmation', methods=['PUT'])
@check_is_admin
def confirm_order():
    try:
        data = request.get_json()
        order_id = data['order']
        order_service = OrderService()
        order_service.confirm_order(order_id)
        return 'OK', 200
    except Exception as error:
        from run import app
        app.logger.error(error)
        return "Error al cargar la orden", 500


@order_cancellation_blueprint.route('/order/cancellation', methods=['PUT'])
@check_is_admin
def cancel_order():
    try:
        data = request.get_json()
        order_id = data['order']
        order_service = OrderService()
        order_service.cancel_order(order_id)
        return 'OK', 200
    except Exception as error:
        from run import app
        app.logger.error(error)
        return "Error al cargar la orden", 500
