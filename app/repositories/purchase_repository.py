from app import db
from app.models.purchase import Purchase


class PurchaseRepository:
    @classmethod
    def save_purchase(cls, user_id, product_id, price, units, color, size, title):
        purchase = Purchase()
        purchase.user_id = user_id
        purchase.product_id = product_id
        purchase.price = price
        purchase.units = units
        purchase.status = 'Activo'
        purchase.features = {'color': color, 'size': size, 'title': title}
        db.session.add(purchase)
        db.session.commit()

    @classmethod
    def get_active_purchases_for_active_user(cls, user_id):
        return Purchase.query.filter_by(user_id=user_id).all()
