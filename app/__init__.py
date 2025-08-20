import logging
import os
from flask import Flask
from .config import Config
from .extensions import db, login_manager, bootstrap, ckeditor, session_ext
from .models import User

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), "templates"),
        static_folder=os.path.join(os.getcwd(), "static"),
    )
    app.config.from_object(Config)


    os.makedirs(app.instance_path, exist_ok=True)
    log_path = os.path.join(app.instance_path, "app.log")
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


    db.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    session_ext.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    from .blueprints.main import main_bp
    from .blueprints.movies import movies_bp
    from .blueprints.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(auth_bp)


    with app.app_context():
        db.create_all()

    return app
