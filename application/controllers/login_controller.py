from flask import Blueprint, request, session, flash, render_template, redirect

from application.services.user_service import UserService

login_blueprint = Blueprint('/login', __name__)
home_blueprint = Blueprint('/', __name__)


@home_blueprint.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect("/register_product")


@login_blueprint.route('/login', methods=['POST'])
def login():
    user_service = UserService()
    response = user_service.login_user(request.form['email'], request.form['password'])
    if response[0]:
        session['logged_in'] = True
        session['user_id'] = response[1]
    else:
        flash('Email o contraseña inválidos')
    return home()
