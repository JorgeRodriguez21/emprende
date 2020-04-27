from flask import Blueprint, request, flash, render_template, redirect, session
from marshmallow import ValidationError

from application.middleware.is_user_logged import check_is_admin
from application.services.product_service import ProductService

register_product_blueprint = Blueprint('/register_product', __name__)
find_product_blueprint = Blueprint('/find_products', __name__)
find_product_by_id_blueprint = Blueprint('/product/<product_id>', __name__)
products_blueprint = Blueprint('/products', __name__)


@register_product_blueprint.route('/register_product', methods=["GET", "POST"])
@check_is_admin
def register_product():
    if request.method == 'POST':
        name = request.form['product_name']
        description = request.form['product_description']
        available_units = request.form['product_available']
        unit_price = request.form['product_unit_price']
        sale_price = request.form['product_sale_price']
        code = request.form['product_code']
        colors = request.form['product_colors']
        sizes = request.form['product_sizes']
        avatar_url = request.form["avatar-url"]
        product_service = ProductService()
        try:
            product_service.register_product(name, description, available_units, unit_price, sale_price, avatar_url,
                                             code, colors, sizes)
            flash('Producto almacenado correctamente')
            return render_template('create_product.html')
        except ValidationError as error:
            flash(error.data)
            from run import app
            app.logger.error(error)
            return render_template('create_product.html')
    else:
        return render_template('create_product.html')


@find_product_blueprint.route('/find_products', methods=["GET"])
@check_is_admin
def register_product():
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
        available_units = request.form['product_available']
        unit_price = request.form['product_unit_price']
        sale_price = request.form['product_sale_price']
        code = request.form['product_code']
        colors = request.form['product_colors']
        sizes = request.form['product_sizes']
        avatar_url = request.form["avatar-url"]
        product_service = ProductService()
        try:
            product_service.register_product(name, description, available_units, unit_price, sale_price, avatar_url,
                                             code, colors, sizes, product_id)
            flash('Producto almacenado correctamente')
            return redirect("/find_products")
        except ValidationError as error:
            flash(error.data)
            from run import app
            app.logger.error(error)
    else:
        product_service = ProductService()
        product = product_service.find_product_by_id(product_id)
        return render_template('edit_product.html', product=product)


@products_blueprint.route('/products', methods=["GET"])
def get_all_products():
    product_service = ProductService()
    products = product_service.find_all_products()
    return render_template('/client_product_list.html', products=products)
