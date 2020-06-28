from flask import Blueprint, request, flash, render_template, redirect, session
from marshmallow import ValidationError
import json
from application.middleware.is_user_logged import check_is_admin
from application.services.product_service import ProductService

register_product_blueprint = Blueprint('/register_product', __name__)
find_product_blueprint = Blueprint('/find_products', __name__)
find_product_by_id_blueprint = Blueprint('/product/<product_id>', __name__)
products_blueprint = Blueprint('/products', __name__)


@register_product_blueprint.route('/register_product', methods=["GET", "POST"])
@check_is_admin
def register_product():
    from run import app
    if request.method == 'POST':
        name = request.form['product_name']
        description = request.form['product_description']
        unit_price = request.form['product_unit_price']
        sale_price = request.form['product_sale_price']
        code = request.form['product_code']
        avatar_url = request.form["avatar-url"]
        status = request.form["product_status"]
        product_id = request.form["prodcut_id"]
        dict_product_details = json.loads(request.form["product_details"])
        product_service = ProductService()
        try:
            product_service.register_product(name, description, unit_price, sale_price, avatar_url,
                                             code, status, dict_product_details, product_id)
            return 'OK', 200
        except ValidationError as error:
            from run import app
            app.logger.error(error)
            return error.messages, 500
    else:
        return render_template('create_product.html')


@find_product_blueprint.route('/find_products', methods=["GET"])
@check_is_admin
def find_products():
    return render_product_list()


def render_product_list():
    product_service = ProductService()
    products = product_service.find_all_products()
    return render_template('find_product.html', products=products)


@find_product_by_id_blueprint.route('/product/<product_id>', methods=["GET", "POST"])
@check_is_admin
def product_by_id(product_id):
    if request.method == 'POST':
        name = request.form['product_name']
        description = request.form['product_description']
        unit_price = request.form['product_unit_price']
        sale_price = request.form['product_sale_price']
        code = request.form['product_code']
        avatar_url = request.form["avatar-url"]
        status = request.form["product_status"]
        dict_product_details = json.loads(request.form["product_details"])
        product_id = request.form["product_id"]
        product_service = ProductService()
        try:
            product_service.register_product(name, description, unit_price, sale_price, avatar_url,
                                             code, status, dict_product_details, product_id)
            return 'OK', 200
        except ValidationError as error:
            from run import app
            app.logger.error(error)
            return error.messages, 500
    else:
        product_service = ProductService()
        product = product_service.find_product_by_id(product_id)
        return render_template('edit_product.html', product=product)


@products_blueprint.route('/products', methods=["GET"])
def get_all_products():
    product_service = ProductService()
    products = product_service.find_all_active_products()
    for product in products:
        json_array = [option.as_dict() for option in product.options]
        product.json_array = json.dumps(json_array)
    return render_template('/client_product_list.html', products=products)
