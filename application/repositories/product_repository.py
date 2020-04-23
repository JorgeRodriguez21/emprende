from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from application.database.database import db
from application.models.Product import Product


class ProductRepository:

    @classmethod
    def save(cls, name, description, available_units, unit_price, sale_price,
             image_name, code, colors, sizes):
        try:
            product = Product(name, description, available_units, unit_price, sale_price,
                              image_name, code, colors, sizes)
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as error:
            from run import app
            app.logger.error('Error de base de datos en productos')
            app.logger.error(error)
            raise ValidationError('Error guardando el producto, por favor intente nuevamente')

    @classmethod
    def update(cls, name, description, available_units, unit_price, sale_price,
               image_name, product_id, code, colors, sizes):
        try:
            product = cls.find_by_id(product_id)
            product.name = name
            product.description = description
            product.available_units = available_units
            product.unit_price = unit_price
            product.sale_price = sale_price
            product.image_name = image_name
            product.code = code
            product.colors = colors
            product.sizes = sizes
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
        ids = cls.get_product_ids(values)
        products = Product.query.filter(Product.id.in_(ids)).all()
        for product_id, units in values:
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
        ids = cls.get_product_ids(values)
        products = Product.query.filter(Product.id.in_(ids)).all()
        for product_id, units in values:
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
