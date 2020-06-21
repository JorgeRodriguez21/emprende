from application.models.ProductOptions import ProductOptions
from application.database.database import db


class ProductOptionsRepository:

    @classmethod
    def delete_all_elements_by_parent_id(cls, product_id):
        results = ProductOptions.query.filter(ProductOptions.product_id == product_id).all()
        from run import app
        for option in results:
            app.logger.error(option.__dict__)
            db.session.delete(option)
        db.session.commit()

    @classmethod
    def update_existent_option(cls, option_id, available_units, product_id):
        option = ProductOptions.query.filter_by(id=option_id).first()
        option.available_units = available_units
        option.product_id = product_id
        from run import app
        app.logger.debug(option.__dict__)
        db.session.commit()

    @classmethod
    def save(cls, available_units, color, size, product_id):
        option = ProductOptions(available_units, color, size)
        option.product_id = product_id
        from run import app
        app.logger.debug(option.__dict__)
        db.session.add(option)
        db.session.commit()
