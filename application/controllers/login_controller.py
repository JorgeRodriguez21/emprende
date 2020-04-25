import json

from flask import Blueprint, request, session, flash, render_template, redirect

from application.services.user_service import UserService

login_blueprint = Blueprint('/login', __name__)
home_blueprint = Blueprint('/', __name__)
roles_blueprint = Blueprint('/roles', __name__)
manage_session_blueprint = Blueprint('/manage_session', __name__)


@home_blueprint.route('/')
def home():
    return redirect("/products")


@roles_blueprint.route('/roles')
def roles():
    return {'isLogged': session.get('logged_in'),
            'isAdmin': session.get('is_admin')}, 200


@login_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_service = UserService()
        response = user_service.login_user(request.form['email'], request.form['password'])
        if response[0]:
            session['logged_in'] = True
            user = response[1]
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['is_admin'] = user.isAdmin
            return redirect("/products")
        else:
            flash('Email o contraseña inválidos')
            return redirect("/login")
    else:
        return render_template('login.html')


@manage_session_blueprint.route('/manage_session', methods=['GET'])
def manage_session():
    if session.get('logged_in'):
        session.clear()
        return json.dumps(True), 200
    else:
        return json.dumps(False), 200
