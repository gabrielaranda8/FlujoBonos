from flask import flash, render_template, redirect, request, Response, url_for, jsonify
from routes.auth import role_required
from utils.remarkets.prices import get_bond_prices
from . import admin

@admin.route("/admin/dashboard")
@role_required(["admin"])
def dashboard():
    bond_prices = get_bond_prices()  # Obtener precios de bonos desde la API
    return render_template("admin/dashboard.html", bond_prices=bond_prices)

@admin.route("/admin/comprar", methods=["POST"])
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


@admin.route("/admin/vender", methods=["POST"])
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
