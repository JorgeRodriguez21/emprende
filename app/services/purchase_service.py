from app.repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    @classmethod
    def create_purchase(cls, user_id, product_id, price, units, color, size, title):
        purchase_repository = PurchaseRepository()
        purchase_repository.save_purchase(user_id, product_id, price, units, color, size, title)

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
        purchase_repository.confirm_purchase(purchase_ids, order_id)
