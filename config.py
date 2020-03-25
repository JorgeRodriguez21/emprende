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
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@db:5432/mybase'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SUPPRESS_SEND = False


class DevelopmentConfig(DefaultConfig):
    @classmethod
    def init_app(cls, app):
        pass

    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': DefaultConfig
}
