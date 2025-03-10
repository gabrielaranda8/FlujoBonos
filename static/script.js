async function procesarOperacion(endpoint, bono) {
    const bonoCard = document.querySelector(`[data-bono="${bono}"]`);
    const montoInput = document.getElementById(`monto-${bono}`);
    const resultadoDiv = document.getElementById(`resultado-${bono}`);
    const monto = parseInt(montoInput.value);

    // Extraer precios del dataset del HTML
    const precioCompra = parseFloat(bonoCard.dataset.precioCompra);
    const precioVenta = parseFloat(bonoCard.dataset.precioVenta);

    if (isNaN(monto) || monto <= 0) {
        resultadoDiv.innerText = "Monto inválido";
        return;
    }

    const data = new FormData();
    if (endpoint === "/admin/comprar") {
        data.append("monto", monto);
        data.append("precio_compra", precioCompra);
    } else if (endpoint === "/admin/vender") {
        // Para vender, enviamos nominales, que es la cantidad de bonos calculada
        const nominales = monto // Calculamos nominales a partir del monto
        data.append("nominales", nominales);
        data.append("precio_venta", precioVenta);
    }

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            body: data
        });

        const result = await response.json();
        if (result.error) {
            resultadoDiv.innerText = result.error;
        } else {
            resultadoDiv.innerText = result['Titulos Comprados'] ? `Titulos Comprados: ${result['Titulos Comprados']}` :
                                     result['Dolares obtenidos'] ? `Dolares obtenidos: ${result['Dolares obtenidos']}` : '';
        }
    } catch (error) {
        resultadoDiv.innerText = "Error en la operación";
    }
}

