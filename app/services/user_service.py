from app.models.User import User
from app.repositories.user_repository import UserRepository


class UserService:

    @classmethod
    def create_user(cls, param_name, param_last_name, param_email, param_password):
        user_repository = UserRepository()
        user_repository.create_user(param_name, param_last_name, param_email, param_password)

    @classmethod
    def login_user(cls, param_email, param_password):
        user_repository = UserRepository()
        user: User = user_repository.find_user_by_email(param_email)
        if user is None:
            return False
        else:
            return user.verify_password(param_password)

    @classmethod
    def recover_user(cls, param_email):
        user_repository = UserRepository()
        return user_repository.update_user_password(param_email)
