# train_model.py

from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

# Ambil dataset California Housing
data = fetch_california_housing(as_frame=True)
df = data.frame

# Fitur dan target
X = df[['MedInc', 'AveRooms', 'HouseAge']]
y = df['MedHouseVal']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Simpan model
joblib.dump(model, 'model.pkl')

print("✅ Saving model on 'model_california_housing.pkl'")