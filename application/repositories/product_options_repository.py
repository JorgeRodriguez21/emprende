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
