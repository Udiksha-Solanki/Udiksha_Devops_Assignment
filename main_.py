from fastapi import FastAPI, Body
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Shipment Delivery Prediction API!"}

# Load the trained model and label encoders
model = joblib.load("model.pkl")
encoder = joblib.load("label_encoders.pkl")

# Define input schema
class ShipmentFeatures(BaseModel):
    Warehouse_block: str
    Mode_of_Shipment: str
    Customer_care_calls: int
    Customer_rating: int
    Cost_of_the_Product: int
    Prior_purchases: int
    Product_importance: str
    Gender: str
    Discount_offered: int
    Weight_in_gms: int

# Prediction endpoint
@app.post("/predict")
def predict(features: ShipmentFeatures = Body(
    ...,
    examples={
        "valid_input": {
            "summary": "Example shipment data",
            "value": {
                "Warehouse_block": "A",
                "Mode_of_Shipment": "Ship",
                "Customer_care_calls": 3,
                "Customer_rating": 4,
                "Cost_of_the_Product": 250,
                "Prior_purchases": 2,
                "Product_importance": "low",
                "Gender": "F",
                "Discount_offered": 20,
                "Weight_in_gms": 1500
            }
        }
    }
)):
    # Convert input to DataFrame
    data = pd.DataFrame([features.dict()])

    # Encode categorical columns
    for col in ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance', 'Gender']:
        le = encoder[col]
        data[col] = le.transform(data[col])

    # Run prediction
    prediction = model.predict(data)

    # Map prediction to label
    prediction_label = "On Time" if prediction[0] == 1 else "Late"

    return {"prediction": prediction_label}
