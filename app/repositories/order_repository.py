from app import db
from app.enums.codes import Codes
from app.enums.order_status import OrderStatus
from app.models.order import Order


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
        return order.id

    @classmethod
    def create_purchase_code(cls, purchase_id):
        code_number = '00' + purchase_id if len(purchase_id) == 1 else '0' + purchase_id if len(
            purchase_id) == 2 else len(purchase_id)
        code = Codes.CODE.value + code_number
        return code
