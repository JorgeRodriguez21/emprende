from flask import Blueprint, request, flash, render_template
from marshmallow import ValidationError

from application.controllers.login_controller import home
from application.services.email_service import EmailService
from application.services.user_service import UserService

create_user_blueprint = Blueprint('/sign_up', __name__)
register_user_blueprint = Blueprint('/register', __name__)
recover_user_blueprint = Blueprint('/recover', __name__)


@create_user_blueprint.route('/sign_up')
def show_signup_page():
    return render_template('create_user.html')


@register_user_blueprint.route('/register', methods=['POST'])
def create_user():
    try:
        user_service = UserService()
        user_service.create_user(request.form['name'], request.form['last_name'], request.form['email'],
                                 request.form['password'])
        return home()
    except ValidationError:
        flash('Email o contraseña inválidos')
        return show_signup_page()


@recover_user_blueprint.route('/recover', methods=["GET", "POST"])
def recover_user():
    if request.method == 'POST':
        email = request.form['email']
        user_service = UserService()
        result = user_service.recover_user(email)
        if result[0] is False:
            flash('Esta cuenta no existe')
        else:
            password = result[1]
            email_service = EmailService()
            email_service.send_email(email, password)
        return home()
    elif request.method == 'GET':
        return render_template('recover_user.html')