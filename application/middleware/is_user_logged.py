from flask import session, redirect, abort, request


def check_logged(func):
    def validation(*args, **kwargs):
        if not ('logged_in' in session and session['logged_in']):
            if request.method == 'POST':
                return 'Debes iniciar sesion para realizar esta accion', 500
            return redirect("/")
        return func(*args, **kwargs)

    return validation


def check_is_admin(func):
    def validation(*args, **kwargs):
        if not ('logged_in' in session and session['logged_in']):
            if request.method == 'POST':
                return 'Debes iniciar sesion para realizar esta accion', 500
            return redirect("/")
        if not session.get('is_admin'):
            abort(401, "No estás autorizado/a a ver este contenido")
        return func(*args, **kwargs)

    return validation
