import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from typing import List, Optional

app = FastAPI(
    title="Sales Prediction API",
    description="API for predicting monthly sales using XGBoost model",
    version="1.0.0"
)

class PredictionInput(BaseModel):
    shop_id: int
    item_id: int
    month_num: int
    year: int
    item_cnt_month_lag_1: Optional[float] = 0
    item_cnt_month_lag_2: Optional[float] = 0
    item_cnt_month_lag_3: Optional[float] = 0

class PredictionResponse(BaseModel):
    prediction: float

try:
    model = joblib.load('model.joblib')
except:
    raise Exception("Model file not found. Please train the model first.")

@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PredictionInput):
    try:
        input_df = pd.DataFrame([input_data.dict()])
        
        prediction = model.predict(input_df)[0]
        
        prediction = np.clip(prediction, 0, 20)
        
        return PredictionResponse(prediction=float(prediction))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Sales Prediction API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 