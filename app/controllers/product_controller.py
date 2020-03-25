from flask import Blueprint, request, flash, render_template
from marshmallow import ValidationError

from app.services.product_service import ProductService

register_product_blueprint = Blueprint('/register_product', __name__)


@register_product_blueprint.route('/register_product', methods=["GET", "POST"])
def register_product():
    if request.method == 'POST':
        name = request.form['product_name']
        description = request.form['product_description']
        available_units = request.form['product_available']
        unit_price = request.form['product_unit_price']
        sale_price = request.form['product_sale_price']
        product_service = ProductService()
        try:
            product_service.register_product(name, description, available_units, unit_price, sale_price, None)
            flash('Producto almacenado correctamente')
            return render_template('create_product.html')
        except ValidationError as error:
            flash(error.data)
            from run import app
            app.logger.error(error)
            return render_template('create_product.html')
    else:
        return render_template('create_product.html')
