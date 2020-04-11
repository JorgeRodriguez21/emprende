from application.repositories.order_repository import OrderRepository


class OrderService:
    @classmethod
    def save_order(cls, code_id, address, city, price):
        order_repository = OrderRepository()
        return order_repository.save_order(code_id, address, city, price)
