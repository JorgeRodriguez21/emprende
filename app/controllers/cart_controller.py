from flask import Blueprint, request, jsonify

cart_controller_blueprint = Blueprint('/add_to_cart', __name__)


@cart_controller_blueprint.route('/add_to_cart', methods=['POST'])
def add_product_to_cart():
    data = request.get_json()
    print(data)
    return jsonify(data)
