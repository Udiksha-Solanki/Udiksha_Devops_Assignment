from fastapi.testclient import TestClient
from main_ import app  # import your FastAPI app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Shipment Delivery Prediction API!"}

def test_prediction():
    sample_input = {
        "Warehouse_block": "A",
        "Mode_of_Shipment": "Flight",
        "Customer_care_calls": 4,
        "Customer_rating": 3,
        "Cost_of_the_Product": 300,
        "Prior_purchases": 3,
        "Product_importance": "low",
        "Gender": "F",
        "Discount_offered": 5,
        "Weight_in_gms": 1234
    }
    response = client.post("/predict", json=sample_input)
    assert response.status_code == 200
    assert "prediction" in response.json()
