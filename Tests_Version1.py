
import pytest
from fastapi.testclient import TestClient
from API_Version2 import app  

# Create the test client
client = TestClient(app)

# Test 1
def test_api_root():
    """Test the root endpoint to ensure API is functional"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is functional"}


# Test 2
def test_predict_delays_valid_request():
    """Test /predict/delays with correctly formatted request"""
    # Sample request parameters (departure airport, arrival airport, departure time, and arrival time)
    response = client.get("/predict/delays", params={
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": "2023-12-10 10:30:00",
        "arrival_time": "2023-12-10 13:30:00"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "average_departure_delay_minutes" in data
    assert isinstance(data["average_departure_delay_minutes"], (int, float))

