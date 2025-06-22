"""Prediction router: Serve ML model predictions for Iris dataset."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import List
import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "model-randomforest.pkl")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

router = APIRouter(
    prefix="/predict",
    tags=["predict"],
    responses={404: {"description": "Not found"}}
)

class PredictionInput(BaseModel):
    data: List[float]

    @field_validator("data")
    @classmethod
    def check_length(cls, v):
        if len(v) != 4:
            raise ValueError("data must contain exactly 4 float values")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "data": [5.1, 3.5, 1.4, 0.2],
            }
        }

class PredictionOutput(BaseModel):
    prediction: int

@router.post("/iris", response_model=PredictionOutput, summary="Predict Iris species")
def predict_iris(input_data: PredictionInput):
    """
    Predict the Iris species using a trained RandomForest model.
    """
    try:
        pred = model.predict([input_data.data])
        return PredictionOutput(prediction=int(pred[0]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))