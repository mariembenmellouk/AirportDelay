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
        "departure_time": "2024-12-10 10:30:00",
        "arrival_time": "2024-12-10 13:30:00"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "average_departure_delay_minutes" in data
    assert isinstance(data["average_departure_delay_minutes"], (int, float))

# Test 3/ Incorrect request
def test_predict_delays_invalid_date_format():
    """Test /predict/delays with invalid date format"""
    response = client.get("/predict/delays", params={
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": "2024-12-10 10-30-00",  # Incorrect date format
        "arrival_time": "2024-12-10 13:30:00"
    })
    
    assert response.status_code == 400  # Bad request due to invalid date format
    assert response.json() == {"detail": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'."}

# Test 4/ Incorrect request 
# GET /predict/delays?departure_airport=JFK&arrival_airport=&departure_time=2024-12-15%2008:00:00&arrival_time=2024-12-15%2011:30:00

