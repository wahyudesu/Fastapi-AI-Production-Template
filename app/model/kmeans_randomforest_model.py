import os
import joblib

# Path ke file model pickle
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model-randomforest.pkl")
model = joblib.load(MODEL_PATH)
print(model)