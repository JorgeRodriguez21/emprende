from collections import Counter

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from application.database.database import db
from application.models.Product import Product
from application.models.ProductOptions import ProductOptions
from application.repositories.product_options_repository import ProductOptionsRepository


class ProductRepository:

    @classmethod
    def save(cls, name, description, unit_price, sale_price,
             image_name, code, options):
        from run import app
        try:
            product = Product(name, description, unit_price, sale_price,
                              image_name, code)
            product_options = []
            for option in options:
                product_option = ProductOptions(int(option['units']), option['color'], option['size'])
                product_options.append(product_option)
            product.options = product_options
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as error:
            app.logger.error('Error de base de datos en productos')
            app.logger.error(error)
            raise ValidationError('Error guardando el producto, por favor intente nuevamente')

    @classmethod
    def update(cls, name, description, unit_price, sale_price,
               image_name, product_id, code, options):
        try:
            product = cls.find_by_id(product_id)
            product.name = name
            product.description = description
            product.unit_price = unit_price
            product.sale_price = sale_price
            product.image_name = image_name
            product.code = code
            product_options = []
            for option in options:
                product_option = ProductOptions(int(option['units']), option['color'], option['size'])
                product_options.append(product_option)
            product.options = product_options
            db.session.commit()
        except SQLAlchemyError as error:
            from run import app
            app.logger.error('Error de base de datos en productos')
            app.logger.error(error)
            raise ValidationError('Error actualizando el producto, por favor intente nuevamente')

    @classmethod
    def find_by_name(cls, name):
        return Product.query.filter(Product.name.ilike(f'%{name}%'))

    @classmethod
    def find_by_id(cls, product_id):
        return Product.query.get(product_id)

    @classmethod
    def find_all(cls):
        return Product.query.order_by(Product.name).all()

    @classmethod
    def get_last_product_id(cls):
        return db.session.query(db.func.max(Product.id)).one()

    @classmethod
    def subtract_purchased_units(cls, values):
        values_without_duplicates = cls.get_product_ids_whit_unified_values(values)
        ids = cls.get_product_ids(values_without_duplicates)
        products = Product.query.filter(Product.id.in_(ids)).all()
        for product_id, units in values_without_duplicates:
            found_product = next(product for product in products if product.id == product_id)
            if found_product is None:
                from run import app
                app.logger.error("Producto con id " + str(product_id) + "no esta disponible")
                raise ValidationError("El producto no está disponible")
            else:
                found_product.available_units = found_product.available_units - int(units)
        db.session.commit()

    @classmethod
    def add_cancelled_units(cls, values):
        values_without_duplicates = cls.get_product_ids_whit_unified_values(values)
        ids = cls.get_product_ids(values_without_duplicates)
        products = Product.query.filter(Product.id.in_(ids)).all()
        for product_id, units in values_without_duplicates:
            found_product = next(product for product in products if product.id == product_id)
            if found_product is None:
                from run import app
                app.logger.error("Producto con id " + str(product_id) + "no esta disponible")
                raise ValidationError("El producto no está disponible")
            else:
                found_product.available_units = found_product.available_units + int(units)

        db.session.commit()

    @classmethod
    def get_product_ids(cls, values):
        ids = []
        for product_id, units in values:
            ids.append(product_id)
        return ids

    @classmethod
    def get_product_ids_whit_unified_values(cls, values):
        count = Counter()
        for i in values:
            count[i[0]] += i[1]
        result = []
        for i in count:
            result.append((i, count[i]))

        return result

    @classmethod
    def check_products_availability(cls, values):
        values_without_duplicates = cls.get_product_ids_whit_unified_values(values)
        ids = cls.get_product_ids(values_without_duplicates)
        products = Product.query.filter(Product.id.in_(ids)).all()
        for product_id, units in values_without_duplicates:
            found_product = next(product for product in products if product.id == product_id)
            if found_product is None:
                from run import app
                app.logger.error("Producto con id " + str(product_id) + "no esta disponible")
                raise ValidationError("El producto no está disponible")
            else:
                remaining_units = found_product.available_units - int(units)
                if remaining_units < 0:
                    raise ValidationError(
                        "El producto " + found_product.name + " no tiene disponibilidad. Por favor eliminelo de su carrito "
                                                              "y mire las unidades disponibles en la pantalla de productos")
