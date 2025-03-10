import os
import logging
from dotenv import load_dotenv
from argparse import ArgumentParser
from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, current_user
from models.base import SessionLocal, init_db
from models import User
from routes.auth.utils import redirect_authenticated_user

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

    init_db()
    create_first_user()

    return app

# from flask import Flask, request, jsonify

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Simulación de precios del bono
# BONO_AL30_PRECIO_ARS = 720.70  # Precio en pesos
# BONO_AL30D_PRECIO_USD = 0.6167  # Precio en dólares

# @app.route('/compra', methods=['POST'])
# def compra_bono():
#     data = request.get_json()
#     monto = data.get('monto')
    
#     if monto is None or monto <= 0:
#         return jsonify({'error': 'El monto debe ser un valor positivo'}), 400
    
#     if monto < BONO_AL30_PRECIO_ARS:
#         return jsonify({'error': f'El monto debe ser mayor o igual a {BONO_AL30_PRECIO_ARS} ARS'}), 400
    
#     nominales = int(monto // BONO_AL30_PRECIO_ARS)  # Solo valores enteros
#     return jsonify({'nominales_comprados': nominales})

# @app.route('/venta', methods=['POST'])
# def venta_bono():
#     data = request.get_json()
#     nominales = data.get('nominales')
    
#     if nominales is None or nominales <= 0:
#         return jsonify({'error': 'La cantidad de nominales debe ser un valor positivo'}), 400
    
#     monto_usd = nominales * BONO_AL30D_PRECIO_USD
#     return jsonify({'monto_obtenido_usd': round(monto_usd, 2)})

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)