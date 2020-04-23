from flask import Blueprint, render_template, request
from marshmallow import ValidationError

from application.middleware.is_user_logged import check_is_admin
from application.services.order_service import OrderService

orders_blueprint = Blueprint('/orders', __name__)
order_detail_blueprint = Blueprint('/order/<order_id>', __name__)
order_confirmation_blueprint = Blueprint('/order/confirmation', __name__)
order_cancellation_blueprint = Blueprint('/order/cancellation', __name__)


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
        return render_template('order_detail.html', order=order)
    except Exception as error:
        from run import app
        app.logger.error(error)
        raise ValidationError("Error al cargar la orden")


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
