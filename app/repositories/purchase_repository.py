from app import db
from app.models.purchase import Purchase


class PurchaseRepository:
    @classmethod
    def save_purchase(cls, user_id, product_id, price, units, color, size):
        purchase = Purchase()
        purchase.user_id = user_id
        purchase.product_id = product_id
        purchase.price = price
        purchase.units = units
        purchase.features = {'color': color, 'size': size}
        db.session.add(purchase)
        db.session.commit()
