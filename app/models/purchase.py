from sqlalchemy.dialects.postgresql import JSONB

from app import db
from app.enums.purchase_status import PurchaseStatus


class Purchase(db.Model):
    __tablename__ = 'purchase'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="cascade"))
    units = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    status = db.Column(db.Enum(PurchaseStatus))
    date = db.Column(db.TIMESTAMP(True))
    features = db.Column(JSONB)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete="cascade"))
