from application.repositories.order_repository import OrderRepository
from application.repositories.product_repository import ProductRepository


class OrderService:
    @classmethod
    def save_order(cls, code_id, address, city, price):
        order_repository = OrderRepository()
        return order_repository.save_order(code_id, address, city, price)

    @classmethod
    def get_all_pending_orders(cls):
        order_repository = OrderRepository()
        return order_repository.find_all_pending_orders()

    @classmethod
    def get_order_by_id(cls, order_id):
        order_repository = OrderRepository()
        return order_repository.find_order_by_id(order_id)

    @classmethod
    def confirm_order(cls, order_id):
        order_repository = OrderRepository()
        order_repository.confirm_order(order_id)

    @classmethod
    def cancel_order(cls, order_id):
        order_repository = OrderRepository()
        id_units = order_repository.cancel_order(order_id)
        product_repository = ProductRepository()
        product_repository.add_cancelled_units(id_units)

    @classmethod
    def save_user_info(cls, order_id, user_info):
        order_repository = OrderRepository()
        order_repository.save_user_info(order_id, user_info)
