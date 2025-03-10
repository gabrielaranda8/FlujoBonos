import pytest
from flask import Flask, jsonify
from routes.auth import role_required
from utils.remarkets.prices import get_bond_prices
from routes.admin import admin
from flask.testing import FlaskClient

# Configuración de la aplicación Flask para las pruebas
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(admin)
    return app

@pytest.fixture
def client(app: FlaskClient):
    return app.test_client()

# Test para el endpoint /admin/dashboard
def test_dashboard(client):
    """Prueba para el endpoint /admin/dashboard"""
    # Simulamos el acceso con un rol adecuado (como admin)
    with client:
        # Suponiendo que role_required es una función que protege la ruta,
        # si el rol no es adecuado, se debería redirigir o devolver error.
        response = client.get('/admin/dashboard')

    # Verificamos que el código de respuesta es 200 (éxito)
    assert response.status_code == 200
    # Verificamos que los precios de los bonos sean renderizados en la respuesta
    assert 'bond_prices' in response.data.decode()

# Test para el endpoint /admin/comprar
@pytest.mark.parametrize("monto, precio_compra, expected_response", [
    (180000, 80220, {"Titulos Comprados": 224}),
    (100000, 50000, {"Titulos Comprados": 200}),
    (50000, 100000, {"error": "El monto debe ser mayor o igual al precio del bono"}),
    (0, 50000, {"error": "Monto o precio inválido"}),
    (180000, -80220, {"error": "Monto o precio inválido"}),
    ("invalid", 80220, {"error": "Entrada no válida"}),
])
def test_comprar(client, monto, precio_compra, expected_response):
    """Prueba para el endpoint /admin/comprar"""
    response = client.post('/admin/comprar', data={
        "monto": monto,
        "precio_compra": precio_compra
    })
    
    # Verificamos que el JSON de respuesta sea el esperado
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == expected_response

# Test para el endpoint /admin/vender
@pytest.mark.parametrize("nominales, precio_venta, expected_response", [
    (224, 80220, {"Dolares obtenidos": 17952.8}),
    (200, 50000, {"Dolares obtenidos": 100000.0}),
    (0, 50000, {"error": "Cantidad de nominales o precio inválido"}),
    ("invalid", 50000, {"error": "Entrada no válida"}),
    (224, -80220, {"error": "Cantidad de nominales o precio inválido"}),
])
def test_vender(client, nominales, precio_venta, expected_response):
    """Prueba para el endpoint /admin/vender"""
    response = client.post('/admin/vender', data={
        "nominales": nominales,
        "precio_venta": precio_venta
    })
    
    # Verificamos que el JSON de respuesta sea el esperado
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == expected_response
