import os


class DefaultConfig:

    @classmethod
    def init_app(cls, app):
        pass

    DEBUG = False
    TESTING = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    CONTACT_PHONE = os.environ['CONTACT_PHONE']
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = 'the random string'


class DevelopmentConfig(DefaultConfig):
    @classmethod
    def init_app(cls, app):
        pass

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@db:5432/mybase'


class ProductionConfig(DefaultConfig):
    @classmethod
    def init_app(cls, app):
        pass

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ['SECRET_KEY']


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
