from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import joinedload

from application.database.database import db
from application.enums.codes import Codes
from application.enums.order_status import OrderStatus
from application.enums.purchase_status import PurchaseStatus
from application.models.order import Order


class OrderRepository:
    @classmethod
    def save_order(cls, code_id, address, city, price):
        order = Order()
        order.code = cls.create_purchase_code(code_id)
        order.status = OrderStatus.PENDING
        order.address = address
        order.city = city
        order.total_price = price
        db.session.add(order)
        db.session.commit()
        return order

    @classmethod
    def create_purchase_code(cls, purchase_id):
        code_number = '00' + purchase_id if len(purchase_id) == 1 else '0' + purchase_id if len(
            purchase_id) == 2 else len(purchase_id)
        code = Codes.CODE.value + code_number
        return code

    @classmethod
    def find_all_pending_orders(cls):
        return Order.query.filter_by(status=OrderStatus.PENDING).all()

    @classmethod
    def find_order_by_id(cls, order_id):
        return Order.query.filter_by(id=order_id).options(joinedload(Order.purchases, innerjoin=True)).first()

    @classmethod
    def save_user_info(cls, order_id, user_info):
        order = cls.find_order_by_id(order_id)
        order.user_info = user_info
        db.session.commit()

    @classmethod
    def confirm_order(cls, order_id):
        order = cls.find_order_by_id(order_id)
        order.status = OrderStatus.CONFIRMED
        for purchase in order.purchases:
            purchase.status = PurchaseStatus.SOLD
        db.session.commit()

    @classmethod
    def cancel_order(cls, order_id):
        id_units = []
        order = cls.find_order_by_id(order_id)
        order.status = OrderStatus.CANCELLED
        for purchase in order.purchases:
            purchase.status = PurchaseStatus.CANCELLED
            purchase.date = datetime.now(timezone(timedelta(hours=-5), 'America/Guayaquil'))
            id_units.append((purchase.product_option_id, purchase.units))
        db.session.commit()
        return id_units
