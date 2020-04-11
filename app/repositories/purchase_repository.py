from datetime import datetime, timezone, timedelta

from app import db
from app.enums.purchase_status import PurchaseStatus
from app.models.purchase import Purchase


class PurchaseRepository:
    @classmethod
    def save_purchase(cls, user_id, product_id, price, units, color, size, title):
        purchase = Purchase()
        purchase.user_id = user_id
        purchase.product_id = product_id
        purchase.price = price
        purchase.units = units
        purchase.status = PurchaseStatus.ACTIVE
        purchase.date = datetime.now(timezone(timedelta(hours=-5), 'America/Guayaquil'))
        purchase.features = {'color': color, 'size': size, 'title': title}
        db.session.add(purchase)
        db.session.commit()

    @classmethod
    def get_active_purchases_for_active_user(cls, user_id):
        return Purchase.query.filter_by(user_id=user_id, status=PurchaseStatus.ACTIVE).all()

    @classmethod
    def cancel_purchase(cls, purchase_id):
        purchase = Purchase.query.filter_by(id=purchase_id).first()
        purchase.status = PurchaseStatus.CANCELLED
        purchase.date = datetime.now(timezone(timedelta(hours=-5), 'America/Guayaquil'))
        db.session.commit()

    @classmethod
    def confirm_purchase(cls, ids, order_id):
        purchases = Purchase.query.filter(Purchase.id.in_(ids)).all()
        if len(purchases) > 0:
            for purchase in purchases:
                purchase.status = PurchaseStatus.CONFIRMED
                purchase.order_id = order_id
                purchase.date = datetime.now(timezone(timedelta(hours=-5), 'America/Guayaquil'))
                db.session.commit()

