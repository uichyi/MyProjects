from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from config import config
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager


bootstrap = Bootstrap5()
db = SQLAlchemy()
mail = Mail()
oauth = OAuth()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'auth.login'


def create_app(config_name="default"):
    app_main = Flask(__name__, template_folder='../FlaskProject/templates', static_folder='../FlaskProject/static')
    app_main.config.from_object(config[config_name])
    config[config_name].init_app(app_main)

    login_manager.init_app(app_main)
    bootstrap.init_app(app_main)
    mail.init_app(app_main)
    db.init_app(app_main)
    migrate.init_app(app_main, db)
    oauth.init_app(app_main)

    from .main import main as main_blueprint
    app_main.register_blueprint(main_blueprint)

    from .auth import auth as auth_bp
    app_main.register_blueprint(auth_bp, url_prefix='/')

    return app_main


from FlaskProject.main import views
