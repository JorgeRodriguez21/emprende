from email_validator import validate_email, EmailNotValidError

from application.models.User import User
from application.repositories.user_repository import UserRepository


class UserService:

    @classmethod
    def create_user(cls, param_name, param_last_name, param_email, param_password, phone):
        user_repository = UserRepository()
        email = validate_email(param_email)
        user_repository.create_user(param_name, param_last_name, email, param_password, phone)

    @classmethod
    def login_user(cls, param_email, param_password):
        user_repository = UserRepository()
        user: User = user_repository.find_user_by_email(param_email)
        if user is None:
            return False, None
        else:
            return user.verify_password(param_password), user

    @classmethod
    def recover_user(cls, param_email):
        user_repository = UserRepository()
        return user_repository.update_user_password(param_email)

    @classmethod
    def validate_email(cls, email):
        v = validate_email(email)
        return v["email"]
