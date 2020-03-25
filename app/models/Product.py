from app.database.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    available_units = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric)
    sale_price = db.Column(db.Numeric)
    image_name = db.Column(db.String(128))

    def __init__(self, name, description, available_units, unit_price, sale_price,
                 image_name):
        super().__init__()
        self.name = name
        self.description = description
        self.available_units = available_units
        self.unit_price = unit_price
        self.sale_price = sale_price,
        self.image_name = image_name
