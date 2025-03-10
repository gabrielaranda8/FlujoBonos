import pyRofex
from config import USER_PRIMARY, PASS_PRIMARY, ACCOUNT_PRIMARY

# Configurar pyRofex con las credenciales leídas desde config.py
pyRofex.initialize(
    user=USER_PRIMARY, 
    password=PASS_PRIMARY, 
    account=ACCOUNT_PRIMARY, 
    environment=pyRofex.Environment.REMARKET
)

# Función para obtener los últimos precios de los bonos
def get_bond_prices():
    instruments = ["MERV - XMEV - AL30 - 24hs", "AL30D/24hs"]
    prices = {}
    
    for instrument in instruments:
        response = pyRofex.get_market_data(
            ticker=instrument, 
            entries=[
                pyRofex.MarketDataEntry.BIDS, 
                pyRofex.MarketDataEntry.OFFERS
            ]
        )
        
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
