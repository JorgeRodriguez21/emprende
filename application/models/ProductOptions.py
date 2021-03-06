import json
from application.database.database import db


class ProductOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    available_units = db.Column(db.Integer)
    color = db.Column(db.String(128))
    size = db.Column(db.String(128))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="cascade", onupdate="cascade"))

    def __init__(self, available_units, color, size):
        super().__init__()
        self.available_units = available_units
        self.color = color
        self.size = size

    def as_dict(self):
        return {
            "id": self.id,
            "available_units": self.available_units,
            "color": self.color,
            "size": self.size
        }
