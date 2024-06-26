import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
import warnings

# Desactivar las advertencias específicas de sklearn
warnings.filterwarnings(action='ignore', category=UserWarning)

# Cargar el modelo y el escalador
rf_model = joblib.load('rf_model.joblib')
scaler = joblib.load('scaler.joblib')

# Definir características
features = ['Price', 'Market cap', 'tvl', 'price_trend', 'market_cap_trend', 'price_volatility', 'tvl_trend']

# Función para predecir el precio de una criptomoneda
def predict_price(data, model, scaler, features):
    data_features = np.array([[data[feature] for feature in features]])
    data_scaled = scaler.transform(data_features)
    prediction = model.predict(data_scaled)
    return "subir" if prediction[0] == 1 else "bajar"

# Función para obtener los datos ingresados y realizar la predicción
def get_prediction():
    try:
        data = {
            'Price': float(entry_price.get()),
            'Market cap': float(entry_market_cap.get()),
            'tvl': float(entry_tvl.get()),
            'price_trend': float(entry_price_trend.get()),
            'market_cap_trend': float(entry_market_cap_trend.get()),
            'price_volatility': float(entry_price_volatility.get()),
            'tvl_trend': float(entry_tvl_trend.get())
        }
        prediction = predict_price(data, rf_model, scaler, features)
        messagebox.showinfo("Predicción", f"El precio va a {prediction}.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# Crear la ventana principal
root = tk.Tk()
root.title("Predicción de Precio de Criptomonedas")

# Crear y ubicar los widgets en la ventana
tk.Label(root, text="Price").grid(row=0, column=0)
entry_price = tk.Entry(root)
entry_price.grid(row=0, column=1)

tk.Label(root, text="Market cap").grid(row=1, column=0)
entry_market_cap = tk.Entry(root)
entry_market_cap.grid(row=1, column=1)

tk.Label(root, text="TVL").grid(row=2, column=0)
entry_tvl = tk.Entry(root)
entry_tvl.grid(row=2, column=1)

tk.Label(root, text="Price trend").grid(row=3, column=0)
entry_price_trend = tk.Entry(root)
entry_price_trend.grid(row=3, column=1)

tk.Label(root, text="Market cap trend").grid(row=4, column=0)
entry_market_cap_trend = tk.Entry(root)
entry_market_cap_trend.grid(row=4, column=1)

tk.Label(root, text="Price volatility").grid(row=5, column=0)
entry_price_volatility = tk.Entry(root)
entry_price_volatility.grid(row=5, column=1)

tk.Label(root, text="TVL trend").grid(row=6, column=0)
entry_tvl_trend = tk.Entry(root)
entry_tvl_trend.grid(row=6, column=1)

tk.Button(root, text="Predecir", command=get_prediction).grid(row=7, column=0, columnspan=2)

# Iniciar el bucle principal de la interfaz
root.mainloop()
