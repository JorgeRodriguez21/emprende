from application.repositories.product_repository import ProductRepository
from application.repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    @classmethod
    def create_purchase(cls, user_id, product_id, price, units, color, size, title, image, option_selected):
        purchase_repository = PurchaseRepository()
        product_repository = ProductRepository()
        product = product_repository.find_by_id(product_id)
        int_units = int(units)
        final_price = product.unit_price * int_units
        from run import app
        if float(price.strip('"')) != final_price:
            app.logger.debug("El precio difiere en back y front " + str(final_price) + " " + str(price))
        purchase_repository.save_purchase(user_id, product_id, final_price, units, color, size, title, image,
                                          option_selected)

    @classmethod
    def get_active_purchases_for_active_user(cls, user_id):
        purchase_repository = PurchaseRepository()
        return purchase_repository.get_active_purchases_for_active_user(user_id)

    @classmethod
    def cancel_purchase(cls, purchase_id):
        purchase_repository = PurchaseRepository()
        purchase_repository.cancel_purchase(purchase_id)

    @classmethod
    def confirm_purchase(cls, purchase_ids, order_id):
        purchase_repository = PurchaseRepository()
        product_repository = ProductRepository()
        id_units = purchase_repository.confirm_purchase(purchase_ids, order_id)
        product_repository.subtract_purchased_units(id_units)
        return purchase_repository.find_purchases_by_ids(purchase_ids)

    @classmethod
    def check_products_availability(cls, ids):
        purchase_repository = PurchaseRepository()
        product_repository = ProductRepository()
        id_units = purchase_repository.get_purchased_units_by_id(ids)
        product_repository.check_products_availability(id_units)

    @classmethod
    def get_last_summary(cls, user_id):
        purchase_repository = PurchaseRepository()
        return purchase_repository.get_last_order_summary(user_id)

    @classmethod
    def update_summary(cls, ids, summary):
        purchase_repository = PurchaseRepository()
        return purchase_repository.update_summary(ids, summary)
