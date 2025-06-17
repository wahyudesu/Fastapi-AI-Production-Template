"""This will serve as a router to make predictions using a machine learning model.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import List

# Import model from app.model.kmeans_randomforest_model
# from app.model.kmeans_randomforest_model import model

import os
import joblib

# Path ke file model pickle
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "model-randomforest.pkl")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

router = APIRouter(prefix="/predict", tags=["predict"])

# Define a Pydantic model for input
class PredictionInput(BaseModel):
    data: List[float]

    # Validator to check if the input list contains 4 values
    @field_validator("data")
    @classmethod
    def check_length(cls, v):
        if len(v) != 4:
            raise ValueError("data must contain exactly 4 float values")
        return v

    # Provide an example schema for documentation
    class Config:
        json_schema_extra = {
            "example": {
                "data": [5.1, 3.5, 1.4, 0.2],
            }
        }

# Define a Pydantic model for output
class PredictionOutput(BaseModel):
    prediction: int

@router.post("/iris", response_model=PredictionOutput)
def predict_iris(input_data: PredictionInput):
    try:
        # Model expects 2D array
        pred = model.predict([input_data.data])
        return PredictionOutput(prediction=int(pred[0]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))