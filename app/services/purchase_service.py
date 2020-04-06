from app.repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    @classmethod
    def create_purchase(cls, user_id, product_id, price, units, color, size):
        purchase_repository = PurchaseRepository()
        purchase_repository.save_purchase(user_id, product_id, price, units, color, size)
