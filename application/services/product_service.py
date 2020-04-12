from marshmallow import ValidationError

from application.repositories.product_repository import ProductRepository


class ProductService:

    @classmethod
    def register_product(cls, name, description, available_units, unit_price, sale_price, image_name, code, colors,
                         sizes, product_id=None):
        try:
            converted_available_units = int(available_units)
            converted_unit_price = float(unit_price)
            converted_sale_price = float(sale_price)
        except ValueError:
            raise ValidationError('Valor no válido, los valores numericos son incorrectos')
        product_repository = ProductRepository()
        if product_id is not None:
            product_repository.update(name, description, available_units, unit_price, sale_price, image_name,
                                      product_id, code, colors, sizes)
        else:
            product_repository.save(name, description, converted_available_units, converted_unit_price,
                                    converted_sale_price,
                                    image_name, code, colors, sizes)

    @classmethod
    def find_products_by_name(cls, name):
        product_repository = ProductRepository()
        return product_repository.find_by_name(name)

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
