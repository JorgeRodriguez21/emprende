from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import db
from app.models.Product import Product
from app.models.User import User, random_string


class ProductRepository:

    @classmethod
    def save(cls, name, description, available_units, unit_price, sale_price,
             image_name):
        try:
            product = Product(name, description, available_units, unit_price, sale_price,
                              image_name)
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as error:
            from run import app
            app.logger.error('Error de base de datos en productos')
            app.logger.error(error)
            raise ValidationError('Error guardando el producto, por favor intente nuevamente')

    @classmethod
    def find_by_name(cls, name):
        return Product.query.filter(Product.name.ilike(f'%{name}%'))

    @classmethod
    def find_all(cls):
        return Product.query.all()
