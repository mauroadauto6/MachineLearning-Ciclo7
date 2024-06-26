import json
import numpy as np
import joblib
import warnings

# Desactivar las advertencias
warnings.filterwarnings("ignore")

# Función para predecir el precio de una criptomoneda
def predict_price(data, model, scaler, features):
    data_features = np.array([[data[feature] for feature in features]])
    data_scaled = scaler.transform(data_features)
    prediction = model.predict(data_scaled)
    return "subir" if prediction[0] == 1 else "bajar"

# Cargar el modelo y el escalador
rf_model = joblib.load('rf_model.joblib')
scaler = joblib.load('scaler.joblib')

# Definir características
features = ['Price', 'Market cap', 'tvl', 'price_trend', 'market_cap_trend', 'price_volatility', 'tvl_trend']

# Cargar nuevos datos desde un archivo JSON
with open('test.json', 'r') as f:
    new_data = json.load(f)

# Realizar predicciones para cada criptomoneda
for token, records in new_data.items():
    for record in records:
        price_trend = predict_price(record, rf_model, scaler, features)
        print(f"El precio de {record['Nombre']} ({token}) va a {price_trend}.")