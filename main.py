from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import os

from keras.src.layers.core.dense import Dense

original_init = Dense.__init__

def patched_init(self, *args, **kwargs):
    if 'quantization_config' in kwargs:
        kwargs.pop('quantization_config')
    original_init(self, *args, **kwargs)

Dense.__init__ = patched_init

app = FastAPI(title="Stock Prediction Backend")

def load_model_safe(name):
    path = os.path.join("models", name)
    if os.path.exists(path):
        try:
            return tf.keras.models.load_model(path, compile=False)
        except Exception as e:
            print(f"Error loading {name}: {e}")
    return None

model_buy = load_model_safe("vn_model_buy_3_1.keras")
model_sell = load_model_safe("vn_model_sell_3_2.keras")

class PredictionRequest(BaseModel):
    data: list

@app.get("/")
def health_check():
    return {"status": "Backend is running", "models_loaded": model_buy is not None}

@app.post("/predict")
async def predict_endpoint(request: PredictionRequest):
    if not model_buy or not model_sell:
        raise HTTPException(status_code=500, detail="Models not loaded on server")
    
    try:
        input_array = np.array(request.data, dtype=np.float32).reshape(1, 60, 5)
        
        buy_res = model_buy.predict(input_array, verbose=0)
        sell_res = model_sell.predict(input_array, verbose=0)
        
        prob_buy = float(buy_res[0][0])
        prob_sell = float(sell_res[0][0])
        
        signal = "HOLD"
        if prob_buy > 0.7: 
            signal = "BUY"
        elif prob_sell > 0.7: 
            signal = "SELL"
        
        return {
            "buy_probability": prob_buy,
            "sell_probability": prob_sell,
            "signal": signal
        }
    except Exception as e:
        print(f"Runtime Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))