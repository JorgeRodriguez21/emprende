import os

from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from sqlalchemy_utils import database_exists, drop_database, create_database

from app.database.database import db
from app.services.email import mail
from config import config


def config_app():
    app = Flask(__name__)
    app.config.from_object(config.get('development'))
    config.get('development').init_app(app)
    db.init_app(app)
    mail.init_app(app)
    environment_debug = os.environ.get("ENV", default='development')
    if environment_debug == 'development':
        with app.app_context():
            app.logger.debug('development')
            CORS(app)
            app.debug = app.config['DEBUG']
            app.logger.debug("before delete database")
            if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
                app.logger.debug('Deleting database.')
                drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
            if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
                app.logger.debug('Creating database.')
                create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            app.logger.debug('Creating tables.')
            app.logger.debug("before create")
            try:
                from app.models.Product import Product
                from app.models.User import User
                db.create_all()
            except BaseException as e:
                app.logger.debug(e)
            app.logger.debug('Shiny!')
    else:
        app.config.from_object('app.config.config.DefaultConfig')
        app.debug = False
        heroku = Heroku(app)
        with app.app_context():
            db.init_app(app)
        mail.init_app(app)
        app.logger.warning('Creating tables. heroku')
        db.create_all()
        app.logger.warning('Shiny! heroku')
    from app.controllers.login_controller import login_blueprint, home_blueprint
    from app.controllers.user_controller import create_user_blueprint, register_user_blueprint, \
        recover_user_blueprint
    from app.controllers.product_controller import register_product_blueprint, find_product_blueprint, \
        find_product_by_id_blueprint, products_blueprint
    from app.controllers.cart_controller import cart_controller_blueprint
    app.register_blueprint(login_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(create_user_blueprint)
    app.register_blueprint(register_user_blueprint)
    app.register_blueprint(recover_user_blueprint)
    app.register_blueprint(register_product_blueprint)
    app.register_blueprint(find_product_blueprint)
    app.register_blueprint(find_product_by_id_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(cart_controller_blueprint)

    return app
