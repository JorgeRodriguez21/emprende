from datetime import datetime, timezone, timedelta

from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from application.database.database import db
from application.enums.purchase_status import PurchaseStatus
from application.models.purchase import Purchase


class PurchaseRepository:
    @classmethod
    def save_purchase(cls, user_id, product_id, price, units, color, size, title, image):
        purchase = Purchase()
        purchase.user_id = user_id
        purchase.product_id = product_id
        purchase.price = price
        purchase.units = units
        purchase.status = PurchaseStatus.ACTIVE
        purchase.date = datetime.now(timezone(timedelta(hours=-5), 'America/Guayaquil'))
        purchase.features = {'color': color, 'size': size, 'title': title, 'image': image}
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
        id_units = []
        purchases = Purchase.query.filter(Purchase.id.in_(ids)).all()
        if len(purchases) > 0:
            for purchase in purchases:
                purchase.status = PurchaseStatus.CONFIRMED
                purchase.order_id = order_id
                purchase.date = datetime.now(timezone(timedelta(hours=-5), 'America/Guayaquil'))
                db.session.commit()
                id_units.append((purchase.product_id, purchase.units))
        return id_units

    @classmethod
    def get_purchased_units_by_id(cls, ids):
        id_units = []
        purchases = Purchase.query.filter(Purchase.id.in_(ids)).all()
        for purchase in purchases:
            id_units.append((purchase.product_id, purchase.units))
        return id_units

    @classmethod
    def update_summary(cls, ids, summary):
        purchases = Purchase.query.filter(Purchase.id.in_(ids)).all()
        if len(purchases) > 0:
            for purchase in purchases:
                purchase.summary = summary
        db.session.commit()

    @classmethod
    def find_purchases_by_ids(cls, ids):
        return Purchase.query.filter(Purchase.id.in_(ids)).options(joinedload(Purchase.user, innerjoin=True)).all()

    @classmethod
    def get_last_order_summary(cls, user_id):
        return Purchase.query.filter_by(user_id=user_id).order_by(desc(Purchase.id)).first().summary
