from sqlalchemy.dialects.postgresql import JSONB

from app import db


class Purchase(db.Model):
    __tablename__ = 'purchase'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="cascade"))
    units = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    status = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    features = db.Column(JSONB)
    purchase_code = db.Column(db.String(10))
