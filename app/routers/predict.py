"""
This will serve as a router to make predictions using a machine learning model.
"""

# predict.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

router = APIRouter(prefix="/predict", tags=["predict"])

# Load model (pastikan path model benar)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/kmeans-clustering.pkl')
model = joblib.load(MODEL_PATH)

class PredictRequest(BaseModel):
    MedInc: float
    AveRooms: float
    HouseAge: float

class PredictResponse(BaseModel):
    prediction: float

@router.post("/house", response_model=PredictResponse)
async def predict_house(request: PredictRequest):
    try:
        input_data = pd.DataFrame({
            'MedInc': [request.MedInc],
            'AveRooms': [request.AveRooms],
            'HouseAge': [request.HouseAge],
        })
        prediction = model.predict(input_data)
        return PredictResponse(prediction=float(prediction[0]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
