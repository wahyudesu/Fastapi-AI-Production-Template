# Contoh prediksi terhadap inputan baru
import numpy as np
import pandas as pd
import joblib

# Load model dari pickle
model = joblib.load('model.pkl')

# Contoh input baru (ganti sesuai fitur yang digunakan pada pelatihan)
input_baru = pd.DataFrame({
    'OverallQual': [7],
    'GrLivArea': [1710],
    'GarageCars': [2],
    'TotalBsmtSF': [856],
})

# Pastikan kolom input_baru sama dengan model
input_baru = input_baru.reindex(columns=model.get_booster().feature_names, fill_value=0)

# Prediksi harga
prediksi_baru = model.predict(input_baru)
print(f'Prediksi harga rumah: {prediksi_baru[0]:.2f}')
