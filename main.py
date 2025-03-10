import os
import logging
from dotenv import load_dotenv
from argparse import ArgumentParser
from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, current_user
from models.base import SessionLocal, init_db
from models import User
from routes.auth.utils import redirect_authenticated_user
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv(override=True)


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
log.disabled = True

ws_config = os.getenv("WS_HOST", "http://127.0.0.1:5000")
invoice_config = os.getenv("ACTIVATE_INVOICE", "True") == "True"

def create_first_user():
    with SessionLocal() as session:
        existing_user = session.query(User).filter_by(username="admin").first()
        if not existing_user:
            session.add(
                User(
                    username="admin",
                    email="admin@example.com",
                    roles=["admin"],
                    password="password",
                )
            )
            session.commit()

def create_app():
    app = Flask(__name__)
    app.debug = os.getenv("DEBUG_ON", "False").lower() == "true"

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 20,
        "pool_size": 30,
        "max_overflow": 10,
    }

    app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Límite de 16 MB
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


    # Configuración de Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with SessionLocal() as session:
            user = session.get(User, int(user_id))
        return user

    # Ruta raíz de la aplicación
    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect_authenticated_user()
        else:
            return redirect(url_for("auth.login"))

    # Importar aquí para evitar referencias circulares
    from routes import blueprints

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # Swagger configuration
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json' 
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Admin API"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    api = Api(app)

    init_db()
    create_first_user()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)