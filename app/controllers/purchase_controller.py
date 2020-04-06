import json

from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from app.services.purchase_service import PurchaseService

purchase_controller_blueprint = Blueprint('/add_to_cart', __name__)


@purchase_controller_blueprint.route('/add_to_cart', methods=['POST'])
def add_product_to_cart():
    try:
        data = request.get_json()
        purchase_service = PurchaseService()
        from run import app
        purchase_service.create_purchase(session['user_id'], data['id'],
                                         data['totalPrice'], data['units'], data['color'],
                                         data['size'])
        return 'OK'
    except Exception as error:
        from run import app
        app.logger.debug(error)
        raise ValidationError("Error saving data")
