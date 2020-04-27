from marshmallow import ValidationError

from application.database.database import db
from application.models.User import User, random_string


class UserRepository:

    @classmethod
    def find_user_by_email(cls, param_email):
        return User.query.filter_by(email=param_email).first()

    @classmethod
    def update_user_password(cls, param_email):
        user = cls.find_user_by_email(param_email)
        if user is None:
            return False, ''
        else:
            new_password = random_string()
            user.password = new_password
            db.session.commit()
            return True, new_password

    @classmethod
    def create_user(cls, param_name, param_last_name, param_email, param_password, phone):
        existent_user = cls.find_user_by_email(param_email)
        if existent_user is None:
            user = User()
            user.password = param_password
            user.email = param_email
            user.phone = phone
            user.name = param_name
            user.last_name = param_last_name
            db.session.add(user)
            db.session.commit()
        else:
            raise ValidationError('Este email ya está registrado')
