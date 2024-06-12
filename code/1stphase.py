import requests
import time
import json

def obtener_gecko_data():
    url = "https://api.llama.fi/v2/chains"
    try:
        response = requests.get(url)
        data = response.json()
        gecko_data = [{"gecko_id": chain.get("gecko_id"), "name": chain.get("name")} for chain in data if chain.get("gecko_id")]
        return gecko_data
    except Exception as e:
        print("Error al obtener los datos:", e)
        return []

def obtener_datos_criptomonedas(gecko_data):
    crypto_data = []
    gecko_ids = set()  # Para almacenar los gecko_id únicos
    for i, chain_data in enumerate(gecko_data, start=1):
        coin_id = chain_data["gecko_id"]
        name = chain_data["name"]
        if coin_id not in gecko_ids:  # Verificar si el gecko_id ya ha sido procesado
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?x_cg_demo_api_key=CG-G5w54s55o7s8A6y7JjESRgMm"
            try:
                response = requests.get(url)
                data = response.json()
                token = data.get("symbol")
                market_cap = data.get("market_data", {}).get("market_cap", {}).get("usd")
                price = data.get("market_data", {}).get("current_price", {}).get("usd")
                categories = data.get("categories", [])
                clase = asignar_clase(categories)

                crypto_data.append({
                    "Token": token,
                    "Nombre": name,
                    "Market cap.": market_cap,
                    "Price": price,
                    "Clase": clase,
                    "gecko_id": coin_id
                })
                gecko_ids.add(coin_id)  # Agregar el gecko_id al conjunto de gecko_ids procesados
                print(f"Criptomoneda agregada al JSON: {name} ({token}) {coin_id}")
            except Exception as e:
                print(f"Error al obtener los datos de {coin_id}:", e)

        # Agregar un retraso de 60 segundos cada 30 monedas analizadas
        if i % 30 == 0 and i != len(gecko_data):
            print("Esperando 60 segundos...")
            time.sleep(60)

    return crypto_data

def asignar_clase(categories):
    for cat in categories:
        if cat == "Artificial Intelligence (AI)":
            return 0
        elif cat == "Gaming (GameFi)":
            return 1
        elif cat == "Real World Assets (RWA)":
            return 2
        elif cat == "Meme":
            return 3
    return 4  # Si no se encontró ninguna categoría de 0 a 3, asignar 4

if __name__ == "__main__":
    gecko_data = obtener_gecko_data()
    if gecko_data:
        datos_criptomonedas = obtener_datos_criptomonedas(gecko_data)
        
        # Guardar datos en un archivo JSON
        with open('criptomonedas.json', 'w') as file:
            json.dump(datos_criptomonedas, file, indent=4)
        print("JSON generado correctamente.")
        
        # Cargar el JSON desde el archivo
        with open('criptomonedas.json', 'r') as file:
            criptomonedas_data = json.load(file)

        # Eliminar gecko_id duplicados
        criptomonedas_data_uniq = [dict(t) for t in {tuple(d.items()) for d in criptomonedas_data}]
        
        # Escribir el JSON sin gecko_id duplicados de nuevo al archivo
        with open('criptomonedas.json', 'w') as file:
            json.dump(criptomonedas_data_uniq, file, indent=4)

        print("Gecko_id duplicados eliminados del JSON.")
        print("Cantidad de elementos en el JSON:", len(criptomonedas_data_uniq))
        
    else:
        print("No se pudo obtener la lista de gecko_ids.")