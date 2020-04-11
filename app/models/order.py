from app.database.database import db
from app.enums.order_status import OrderStatus


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    total_price = db.Column(db.Numeric)
    city = db.Column(db.String(50))
    address = db.Column(db.String(300))
    status = db.Column(db.Enum(OrderStatus))
    purchases = db.relationship("Purchase", lazy=False,
                                backref=db.backref("order", lazy=False))
