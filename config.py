# encoding:utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess thing '
    FLASKY_MAIL_SENDER = '[Flasky]'
    FLASKY_MAIL_SUBJECT_PREFIX = '<Flasky Admin <18515061990@sina.cn>>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = 'True'
    MAIL_USERNAME = '18515061990@sina.cn'
    MAIL_PASSWORD = '18515061990flask'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')



class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
