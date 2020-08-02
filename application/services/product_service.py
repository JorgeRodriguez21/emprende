from marshmallow import ValidationError

from application.repositories.product_options_repository import ProductOptionsRepository
from application.repositories.product_repository import ProductRepository


class ProductService:

    @classmethod
    def register_product(cls, name, description, unit_price, sale_price, image_name, code, status, options,
                         product_id):
        boolean_status = True if status == 'Activo' else False
        try:
            converted_unit_price = float(unit_price)
            converted_sale_price = float(sale_price)
        except ValueError:
            raise ValidationError('Valor no válido, los valores numericos son incorrectos')
        product_repository = ProductRepository()
        if int(product_id) > 0:
            product_repository.update(name, description, converted_unit_price, converted_sale_price, image_name,
                                      product_id, code, boolean_status, options)
        else:
            product_repository.save(name, description, converted_unit_price,
                                    converted_sale_price,
                                    image_name, code, boolean_status, options)

    @classmethod
    def find_products_by_name(cls, name):
        product_repository = ProductRepository()
        return product_repository.find_by_name(name)

    @classmethod
    def find_all_active_products(cls):
        product_repository = ProductRepository()
        return product_repository.find_all_active()

    @classmethod
    def find_all_products(cls):
        product_repository = ProductRepository()
        return product_repository.find_all()

    @classmethod
    def find_product_by_id(cls, product_id):
        product_repository = ProductRepository()
        return product_repository.find_by_id(product_id)

    @classmethod
    def find_last_id(cls):
        product_repository = ProductRepository()
        return product_repository.get_last_product_id()

    @classmethod
    def find_all_products_by_ids(cls, product_ids):
        product_repository = ProductRepository()
        return product_repository.find_all_products_by_ids(product_ids)
