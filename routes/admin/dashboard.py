import pyRofex
from flask import flash, render_template, redirect, request, Response, url_for, jsonify
from routes.auth import role_required
from . import admin

@admin.route("/admin/dashboard")
@role_required(["admin"])
def dashboard():
    bond_prices = get_bond_prices()  # Obtener precios de bonos desde la API
    return render_template("admin/dashboard.html", bond_prices=bond_prices)

@admin.route("/admin/comprar", methods=["GET", "POST"])
def comprar():
    try:
        monto = int(request.form.get("monto", 0))
        precio_compra = float(request.form.get("precio_compra", 0))  # Viene del frontend

        if monto <= 0 or precio_compra <= 0:
            return jsonify({"error": "Monto o precio inválido"}), 400

        if monto < precio_compra:
            return jsonify({"error": "El monto debe ser mayor o igual al precio del bono"}), 400

        nominales = int((monto*100) / precio_compra) # multiplicamos por 100 para ajustarlo al valor nominal

        return jsonify({"Titulos Comprados": nominales})

    except (ValueError, TypeError):
        return jsonify({"error": "Entrada no válida"}), 400


@admin.route("/admin/vender", methods=["GET", "POST"])
def vender():
    try:
        nominales = int(request.form.get("nominales", 0))  # Ahora recibe nominales en lugar de monto
        precio_venta = float(request.form.get("precio_venta", 0))  # Precio del bono

        if nominales <= 0 or precio_venta <= 0:
            return jsonify({"error": "Cantidad de nominales o precio inválido"}), 400

        # Ajuste por la cotización de los bonos (valor nominal de 100)
        dolares_obtenidos = ((nominales/100) * precio_venta)  # dividimos por 100 para ajustarlo al valor nominal

        return jsonify({"Dolares obtenidos": round(dolares_obtenidos, 2)})

    except (ValueError, TypeError):
        return jsonify({"error": "Entrada no válida"}), 400




# Configurar pyRofex con credenciales
pyRofex.initialize(user="gabrielaranda820753", password="jqelpJ2$", account="REM20753", environment=pyRofex.Environment.REMARKET)

# Función para obtener los últimos precios de los bonos
def get_bond_prices():
    instruments = ["MERV - XMEV - AL30 - 24hs", "AL30D/24hs"]
    prices = {}
    
    for instrument in instruments:
        response = pyRofex.get_market_data(ticker=instrument, entries=[
            pyRofex.MarketDataEntry.BIDS,
            pyRofex.MarketDataEntry.OFFERS
        ])
        
        if "marketData" in response:
            market_data = response["marketData"]
            if instrument == "MERV - XMEV - AL30 - 24hs":
                default_compra, default_venta = 80225, 80220
            else:  # AL30D/24hs
                default_compra, default_venta = 65.65, 65.61
            
            prices[instrument] = {
                "compra": market_data["BI"][0]["price"] if "BI" in market_data and market_data["BI"] else default_compra,
                "venta": market_data["OF"][0]["price"] if "OF" in market_data and market_data["OF"] else default_venta
            }
    
    return prices
