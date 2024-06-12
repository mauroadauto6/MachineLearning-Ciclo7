import requests
import json
from datetime import datetime

def extraer_nombres_gecko_id(archivo_json):
    nombres_gecko_id_diccionario = {}

    with open(archivo_json, 'r') as archivo:
        datos = json.load(archivo)
        for criptomoneda in datos:
            gecko_id = criptomoneda.get('gecko_id')
            nombre = criptomoneda.get('Nombre')
            if gecko_id and nombre:
                nombres_gecko_id_diccionario[nombre] = gecko_id

    return nombres_gecko_id_diccionario

def obtener_historial_tvl(nombre_criptomoneda):
    url = f'https://api.llama.fi/v2/historicalChainTvl/{nombre_criptomoneda}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"No se pudo obtener el historial de TVL para {nombre_criptomoneda}.")
        return None

def formatear_fecha(timestamp):
    fecha = datetime.utcfromtimestamp(timestamp)
    return fecha.strftime('%d/%m/%Y')

def obtener_historial_tvl_periodo(historial_tvl):
    if 'statusCode' in historial_tvl and historial_tvl['statusCode'] == 400:
        print(f"No hay historial de TVL disponible para esta criptomoneda.")
        return []
    else:
        historial_tvl_periodo = []
        for registro in historial_tvl:
            if registro['date'] >= 1696136400 and registro['date'] <= 1714539600:  # Periodo del 1 de octubre de 2023 al 1 de mayo de 2024
                registro_formateado = {
                    "date": formatear_fecha(registro['date']),
                    "tvl": registro['tvl']
                }
                historial_tvl_periodo.append(registro_formateado)
        return historial_tvl_periodo

def cargar_datos_criptomonedas(archivo_json):
    with open(archivo_json, 'r') as archivo:
        return json.load(archivo)

def agregar_info_criptomoneda_a_historial(datos_criptomonedas, historial_tvl):
    historial_actualizado = {}
    for criptomoneda in datos_criptomonedas:
        nombre_criptomoneda = criptomoneda.get("Nombre")
        gecko_id = criptomoneda.get("gecko_id")
        token = criptomoneda.get("Token")
        clase = criptomoneda.get("Clase")
        historial = historial_tvl.get(nombre_criptomoneda, [])
        historial_con_info = [{"date": registro["date"], "tvl": registro["tvl"], "Token": token, "Nombre": nombre_criptomoneda, "Clase": clase} for registro in historial]
        historial_actualizado[gecko_id] = historial_con_info
    return historial_actualizado

if __name__ == "__main__":
    # Ruta del archivo JSON de criptomonedas
    archivo_json_criptomonedas = 'criptomonedas.json'
    
    # Obtener nombres y gecko_id
    nombres_gecko_id_diccionario = extraer_nombres_gecko_id(archivo_json_criptomonedas)
    
    # Diccionario para almacenar historial de TVL
    historial_tvl_diccionario = {}
    
    # Obtener historial de TVL para cada criptomoneda y almacenarlo en el diccionario
    for nombre_criptomoneda, gecko_id in nombres_gecko_id_diccionario.items():
        print(f"Agregando historial de TVL para {nombre_criptomoneda}...")
        historial_tvl = obtener_historial_tvl(nombre_criptomoneda)
        if historial_tvl:
            historial_tvl_periodo = obtener_historial_tvl_periodo(historial_tvl)
            historial_tvl_diccionario[nombre_criptomoneda] = historial_tvl_periodo
            print(f"Historial de TVL para {nombre_criptomoneda} agregado correctamente.")
    
    # Agregar información de criptomonedas al historial de TVL
    datos_criptomonedas = cargar_datos_criptomonedas(archivo_json_criptomonedas)
    historial_tvl_con_info = agregar_info_criptomoneda_a_historial(datos_criptomonedas, historial_tvl_diccionario)
    
    # Guardar el historial actualizado en un archivo JSON
    with open('historial_tvl_criptomonedas.json', 'w') as archivo_salida:
        json.dump(historial_tvl_con_info, archivo_salida, indent=4)
    
    print("El historial de TVL actualizado con información de criptomonedas se ha guardado en 'historial_tvl_criptomonedas.json'")
