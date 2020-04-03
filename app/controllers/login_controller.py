from flask import Blueprint, request, session, flash, render_template, redirect

from app.services.user_service import UserService

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
    if user_service.login_user(request.form['email'], request.form['password']):
        session['logged_in'] = True
        session['user'] = request.form['email']
    else:
        flash('Email o contraseña inválidos')
    return home()
