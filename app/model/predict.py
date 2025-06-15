# predict.py

import joblib
import pandas as pd

# Load model
model = joblib.load('model_california_housing.pkl')

# Contoh input data: Median Income, Average Rooms, House Age
input_data = pd.DataFrame({
    'MedInc': [8.3252],    # median income
    'AveRooms': [6.9841],  # average number of rooms
    'HouseAge': [15.0],    # house age
})

# Prediksi
prediction = model.predict(input_data)

print(f"💰 Prediksi harga rumah: {prediction[0]:.2f} (dalam ratusan ribu USD)")
