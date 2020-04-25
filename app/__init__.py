import os

from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from sqlalchemy_utils import database_exists, create_database, drop_database

from application.controllers.purchase_controller import purchase_delete_blueprint, purchase_confirm_blueprint
from application.database.database import db
from application.services.email import mail
from config import config


def config_app():
    app = Flask(__name__, template_folder="../application/templates", static_folder='../application/static')
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
            # app.logger.debug("before delete database")
            # if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            #     app.logger.debug('Deleting database.')
            #     drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
            if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
                app.logger.debug('Creating database.')
                create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            app.logger.debug('Creating tables.')
            app.logger.debug("before create")
            try:
                create_tables()
            except BaseException as e:
                app.logger.debug(e)
            app.logger.debug('Shiny!')
    else:
        app.config.from_object(config.get('production'))
        app.debug = False
        heroku = Heroku(app)
        with app.app_context():
            db.init_app(app)
            mail.init_app(app)
            app.logger.warning('Creating tables. heroku')
            create_tables()
            app.logger.warning('Shiny! heroku')
    register_blueprints(app)
    return app


def register_blueprints(app):
    from application.controllers.login_controller import login_blueprint, home_blueprint, \
        roles_blueprint, manage_session_blueprint
    from application.controllers.user_controller import create_user_blueprint, register_user_blueprint, \
        recover_user_blueprint
    from application.controllers.product_controller import register_product_blueprint, find_product_blueprint, \
        find_product_by_id_blueprint, products_blueprint
    from application.controllers.purchase_controller import purchase_blueprint, purchase_list_blueprint
    from application.controllers.aws_controller import sign_s3_blueprint
    from application.controllers.order_controller import orders_blueprint, order_detail_blueprint, \
        order_confirmation_blueprint, order_cancellation_blueprint
    app.register_blueprint(login_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(create_user_blueprint)
    app.register_blueprint(register_user_blueprint)
    app.register_blueprint(recover_user_blueprint)
    app.register_blueprint(register_product_blueprint)
    app.register_blueprint(find_product_blueprint)
    app.register_blueprint(find_product_by_id_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(purchase_blueprint)
    app.register_blueprint(purchase_list_blueprint)
    app.register_blueprint(purchase_delete_blueprint)
    app.register_blueprint(purchase_confirm_blueprint)
    app.register_blueprint(sign_s3_blueprint)
    app.register_blueprint(orders_blueprint)
    app.register_blueprint(order_detail_blueprint)
    app.register_blueprint(order_confirmation_blueprint)
    app.register_blueprint(order_cancellation_blueprint)
    app.register_blueprint(roles_blueprint)
    app.register_blueprint(manage_session_blueprint)


def create_tables():
    from application.models.User import User
    from application.models.Product import Product
    from application.models.order import Order
    from application.models.purchase import Purchase
    db.create_all()
