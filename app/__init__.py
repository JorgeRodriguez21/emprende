import os

from flask import Flask
from flask_cors import CORS
from app.database.database import db
from config import config
from app.services.email import mail


def config_app():
    app = Flask(__name__)
    app.config.from_object(config.get('development'))
    config.get('development').init_app(app)
    db.init_app(app)
    mail.init_app(app)

    # mail_settings = {
    #     "MAIL_SERVER": 'smtp.gmail.com',
    #     "MAIL_PORT": 465,
    #     "MAIL_USE_TLS": False,
    #     "MAIL_USE_SSL": True,
    #     "MAIL_USERNAME": os.environ['EMAIL_USER'],
    #     "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
    # }
    # app.config.update(mail_settings)
    CORS(app)
    ENVIRONMENT_DEBUG = os.environ.get("ENV", default='development')
    if ENVIRONMENT_DEBUG == 'development':
        with app.app_context():
            from sqlalchemy_utils import database_exists, drop_database, create_database
            from app.controllers.login_controller import login_blueprint, home_blueprint
            from app.controllers.user_controller import create_user_blueprint, register_user_blueprint, \
                recover_user_blueprint
            app.config.from_object(config['development'])
            config['development'].init_app(app)
            app.logger.debug('Entra al if de development')
            app.logger.debug(app.config['DEBUG'])
            app.debug = app.config['DEBUG']

            app.logger.debug(app.config['DEBUG'])
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
                db.create_all()
            except BaseException as e:
                app.logger.debug(e)
            app.logger.debug('Shiny!')
            # else:
            #     app.config.from_object('app.config.config.DefaultConfig')
            #     app.debug = False
            #     heroku = Heroku(app)
            #     with app.app_context():
            #         db.init_app(app)
            #         mail.init_app(app)
            #         app.logger.warning('Creating tables. heroku')
            #         db.create_all()
            #         app.logger.warning('Shiny! heroku')

            app.register_blueprint(login_blueprint)
            app.register_blueprint(home_blueprint)
            app.register_blueprint(create_user_blueprint)
            app.register_blueprint(register_user_blueprint)
            app.register_blueprint(recover_user_blueprint)

    return app
