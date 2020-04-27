from application.database.database import db
from application.enums.order_status import OrderStatus


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10))
    total_price = db.Column(db.Numeric)
    city = db.Column(db.String(50))
    address = db.Column(db.String(300))
    status = db.Column(db.Enum(OrderStatus))
    user_info = db.Column(db.String(300))
    purchases = db.relationship("Purchase",
                                backref=db.backref("order", lazy='joined'))
