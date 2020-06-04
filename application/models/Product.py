from application.database.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    unit_price = db.Column(db.Numeric)
    sale_price = db.Column(db.Numeric)
    image_name = db.Column(db.String(128))
    code = db.Column(db.String(128))
    users = db.relationship("User",
                            secondary="purchase",
                            backref=db.backref("product"))
    options = db.relationship("ProductOptions",
                                backref=db.backref("product", lazy='joined'))

    def __init__(self, name, description, unit_price, sale_price,
                 image_name, code):
        super().__init__()
        self.name = name
        self.description = description
        self.unit_price = unit_price
        self.sale_price = sale_price,
        self.image_name = image_name
        self.code = code
