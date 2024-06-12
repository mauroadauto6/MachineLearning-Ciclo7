import json
import requests
from datetime import datetime
import time
import numpy as np

def obtener_datos_tvls_precios_gecko_ids():
    # Leer el archivo JSON y obtener todos los gecko_id
    with open("historial_tvl_criptomonedas.json", "r") as file:
        tvl_info_data = json.load(file)

    gecko_ids = list(tvl_info_data.keys())

    # Obtener los datos de precio y market cap para cada gecko_id en el rango de fechas especificado
    url = "https://api.coingecko.com/api/v3/coins/{}/market_chart/range?x_cg_demo_api_key=CG-G5w54s55o7s8A6y7JjESRgMm"

    # Definir las fechas de inicio y fin en formato Unix timestamp
    start_date = 1696136400  # 01 de octubre de 2023
    end_date = 1714539600    # 01 de mayo de 2024

    # Diccionario para almacenar los datos de precio y market cap por gecko_id
    combined_data = {}

    # Contador para controlar el retraso
    call_count = 0

    for gecko_id in gecko_ids:
        # Añadir un retraso de 60 segundos cada 30 llamadas
        if call_count % 30 == 0 and call_count != 0:
            print("Esperando 60 segundos para evitar sobrecargar la API...")
            time.sleep(60)

        params = {
            "vs_currency": "usd",
            "from": start_date,
            "to": end_date
        }
        response = requests.get(url.format(gecko_id), params=params)
        call_count += 1

        if response.status_code == 200:
            data = response.json()
            prices = data['prices']
            market_caps = data['market_caps']
            # Convertir el formato de fecha Unix a dd/mm/yyyy
            formatted_prices = [(datetime.utcfromtimestamp(timestamp / 1000).strftime('%d/%m/%Y'), price) for timestamp, price in prices]
            formatted_market_caps = [(datetime.utcfromtimestamp(timestamp / 1000).strftime('%d/%m/%Y'), market_cap) for timestamp, market_cap in market_caps]
            # Almacenar los datos en el diccionario
            combined_data[gecko_id] = {"prices": formatted_prices, "market_caps": formatted_market_caps}
            print(f"Datos de {gecko_id} añadidos correctamente.")
        else:
            print(f"Error al obtener datos para {gecko_id}: {response.status_code}")

    # Leer el primer archivo JSON
    with open("historial_tvl_criptomonedas.json", "r") as file:
        tvl_info_data = json.load(file)

    # Nuevo diccionario para almacenar los datos combinados
    combined_data_final = {}

    # Combinar la información de ambos conjuntos de datos
    for criptomoneda, info in tvl_info_data.items():
        if criptomoneda in combined_data:
            combined_data_final[criptomoneda] = []
            for entry in info:
                date = entry["date"]
                tvl = entry["tvl"]
                token = entry["Token"]
                nombre = entry["Nombre"]
                clase = entry["Clase"]
                prices = combined_data[criptomoneda]["prices"]
                market_caps = combined_data[criptomoneda]["market_caps"]
                for price_entry, market_cap_entry in zip(prices, market_caps):
                    if price_entry[0] == date and market_cap_entry[0] == date:
                        price = price_entry[1]
                        market_cap = market_cap_entry[1]
                        combined_data_final[criptomoneda].append({
                            "date": date,
                            "Price": price,
                            "Market cap": market_cap,
                            "tvl": tvl,
                            "Token": token,
                            "Nombre": nombre,
                            "Clase": clase
                        })
                        break

    # Eliminar criptomonedas sin contenido
    combined_data_final = {criptomoneda: registros for criptomoneda, registros in combined_data_final.items() if registros}

    # Calcular correlaciones
    threshold = 0.7
    correlation_results = {}

    for criptomoneda, registros in combined_data_final.items():
        tvl = []
        market_cap = []
        price = []

        for registro in registros:
            tvl.append(registro.get('tvl', np.nan))
            market_cap.append(registro.get('Market cap', np.nan))
            price.append(registro.get('Price', np.nan))

        if len(tvl) >= 2 and len(market_cap) >= 2 and len(price) >= 2:
            correlation_matrix = np.corrcoef([tvl, market_cap, price])
            correlation_coefficient = correlation_matrix[0, 1]

            if np.isnan(correlation_coefficient):
                correlation_results[criptomoneda] = 1  # No hay suficientes datos para calcular la correlación
            elif abs(correlation_coefficient) >= threshold:
                correlation_results[criptomoneda] = 0  # Hay correlación significativa
            else:
                correlation_results[criptomoneda] = 1  # No hay correlación significativa
        else:
            correlation_results[criptomoneda] = 1  # No hay suficientes datos para calcular la correlación

    # Actualizar el JSON original con los resultados de correlación
    for criptomoneda, registros in combined_data_final.items():
        for registro in registros:
            registro['correlacion'] = correlation_results[criptomoneda]

    # Guardar el JSON actualizado con los resultados de correlación
    with open('dataset.json', 'w') as file:
        json.dump(combined_data_final, file, indent=4)

    print("Datos combinados y guardados en 'dataset.json'")

if __name__ == "__main__":
    obtener_datos_tvls_precios_gecko_ids()