from numbers import Number

from marshmallow import ValidationError

from app.repositories.product_repository import ProductRepository


class ProductService:

    @classmethod
    def register_product(cls, name, description, available_units, unit_price, sale_price, image_name):
        try:
            converted_available_units = int(available_units)
            converted_unit_price = float(unit_price)
            converted_sale_price = float(sale_price)
        except ValueError:
            raise ValidationError('Valor no válido, los valores numericos son incorrectos')
        product_repository = ProductRepository()
        product_repository.save(name, description, converted_available_units, converted_unit_price,
                                converted_sale_price,
                                image_name)

    @classmethod
    def find_products_by_name(cls, name):
        product_repository = ProductRepository()
        return product_repository.find_by_name(name)

    @classmethod
    def find_all_products(cls):
        product_repository = ProductRepository()
        return product_repository.find_all()