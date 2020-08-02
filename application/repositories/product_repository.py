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
             image_name, code, status, options):
        try:
            product = Product(name, description, unit_price, sale_price,
                              image_name, code, status)
            product_options = []
            for option in options:
                product_option = ProductOptions(int(option['units']), option['color'], option['size'])
                product_options.append(product_option)
            product.options = product_options
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as error:
            from run import app
            app.logger.error('Error de base de datos en productos')
            app.logger.error(error)
            raise ValidationError('Error guardando el producto, por favor intente nuevamente')

    @classmethod
    def update(cls, name, description, unit_price, sale_price,
               image_name, product_id, code, status, options):
        product_option_repository = ProductOptionsRepository()
        try:
            product = cls.find_by_id(product_id)
            product.name = name
            product.description = description
            product.unit_price = unit_price
            product.sale_price = sale_price
            product.image_name = image_name
            product.code = code
            product.is_active = status
            db.session.commit()
            for option in options:
                option_id = int(option['id'])
                if option_id > 0:
                    product_option_repository.update_existent_option(option_id, int(option['units']), product_id)
                else:
                    product_option_repository.save(int(option['units']), option['color'], option['size'], product_id)
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
    def find_all_active(cls):
        return Product.query.filter_by(is_active=True).order_by(Product.name).all()

    @classmethod
    def find_all(cls):
        return Product.query.order_by(Product.name).all()

    @classmethod
    def get_last_product_id(cls):
        return db.session.query(db.func.max(Product.id)).one()

    @classmethod
    def subtract_purchased_units(cls, values):
        values_without_duplicates = cls.get_product_options_ids_with_unified_values(values)
        ids = cls.get_product_option_ids(values_without_duplicates)
        products_options = ProductOptions.query.filter(ProductOptions.id.in_(ids)).all()
        for product_option_id, units in values_without_duplicates:
            found_product_options = next(
                product_option for product_option in products_options if product_option.id == product_option_id)
            if found_product_options is None:
                from run import app
                app.logger.error("Product_option con id " + str(product_option_id) + "no esta disponible")
                raise ValidationError("El producto no está disponible")
            else:
                found_product_options.available_units = found_product_options.available_units - int(units)
        db.session.commit()

    @classmethod
    def add_cancelled_units(cls, values):
        values_without_duplicates = cls.get_product_options_ids_with_unified_values(values)
        ids = cls.get_product_option_ids(values_without_duplicates)
        products_options = ProductOptions.query.filter(ProductOptions.id.in_(ids)).all()
        for product_option_id, units in values_without_duplicates:
            found_product_options = next(
                product_option for product_option in products_options if product_option.id == product_option_id)
            if found_product_options is None:
                from run import app
                app.logger.error("Product_option con id " + str(product_option_id) + "no esta disponible")
                raise ValidationError("El producto no está disponible")
            else:
                found_product_options.available_units = found_product_options.available_units + int(units)
        db.session.commit()

    @classmethod
    def get_product_option_ids(cls, values):
        ids = []
        for product_option_id, units in values:
            ids.append(product_option_id)
        return ids

    @classmethod
    def get_product_ids_from_product_options(cls, options):
        ids = []
        for product_option in options:
            ids.append(product_option.product_id)
        return ids

    @classmethod
    def get_product_options_ids_with_unified_values(cls, values):
        count = Counter()
        for i in values:
            count[i[0]] += i[1]
        result = []
        for i in count:
            result.append((i, count[i]))

        return result

    @classmethod
    def check_products_availability(cls, values):
        from run import app
        values_without_duplicates = cls.get_product_options_ids_with_unified_values(values)
        app.logger.debug("Values without duplicates")
        app.logger.debug(values_without_duplicates)
        ids = cls.get_product_option_ids(values_without_duplicates)
        app.logger.debug("Ids")
        app.logger.debug(ids)
        product_options = ProductOptions.query.filter(ProductOptions.id.in_(ids)).all()
        app.logger.debug("product options")
        app.logger.debug(product_options)
        products = Product.query.filter(Product.id.in_(cls.get_product_ids_from_product_options(product_options))).all()
        app.logger.debug("products")
        app.logger.debug(products)
        for product_option_id, units in values_without_duplicates:
            found_product_option = next(
                product_option for product_option in product_options if product_option.id == product_option_id)
            if found_product_option is None:
                from run import app
                app.logger.error("Producto con id " + str(product_option_id) + "no esta disponible")
                raise ValidationError("El producto no está disponible")
            else:
                remaining_units = found_product_option.available_units - int(units)
                app.logger.debug("remaining units")
                app.logger.debug(remaining_units)
                if remaining_units < 0:
                    found_product = next(
                        (product for product in products if
                         product.id == found_product_option.product_id), None)
                    raise ValidationError(
                        "El producto " + found_product.name + " en color " + found_product_option.color + " y en talla "
                        + found_product_option.size + " no tiene disponibilidad. Por favor eliminelo de su carrito "
                                                      "y mire las unidades disponibles en la pantalla de productos")

    @classmethod
    def find_all_products_by_ids(cls, product_ids):
        return Product.query.filter(Product.id.in_(product_ids)).all()
