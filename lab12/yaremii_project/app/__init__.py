from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    ckeditor.init_app(app)


    with app.app_context():
        from app.home import home_bp
        from app.contact import contact_bp
        from app.account import account_bp
        from app.task import task_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(contact_bp)
        app.register_blueprint(account_bp)
        app.register_blueprint(task_bp)


    return app
