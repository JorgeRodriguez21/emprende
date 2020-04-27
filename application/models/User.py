import bcrypt
import random
import string
from flask_login import UserMixin

from application.database.database import db


def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128))
    isAdmin = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20))
    products = db.relationship("Product",
                               secondary="purchase",
                               backref=db.backref("user"))

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        bvalue = bytes(password, 'utf-8')
        password_hash = bcrypt.hashpw(bvalue, bcrypt.gensalt())
        self.password_hash = password_hash.decode('utf8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
