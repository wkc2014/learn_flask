from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config

login_manager = LoginManager()
login_manager.session_protection = 'Strong'
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
pagedown = PageDown()


def html_tag_filter(html_content):
    result = html_content.replace('#', '').replace('<pre>', '').replace('</pre>', '')
    return result


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    csrf.init_app(app)

    app.add_template_filter(html_tag_filter, 'html_tag_filter')

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
