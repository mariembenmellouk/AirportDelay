#!/usr/bin/env python
# coding: utf-8

# import statements
from fastapi import FastAPI, HTTPException
import json
import numpy as np
import pickle
import datetime

# Initialize FastAPI app
app = FastAPI()

# Import the json file for airports encoding
with open('airport_encodings.json', 'r') as f:
    airports = json.load(f)

# Function to create one-hot encoding for the airports
def create_airport_encoding(airport: str, airports: dict) -> np.array:
    """
    Creates a one-hot encoded array for the specified arrival airport.
    The array has all zeros except for the one corresponding to the specified arrival airport.

    Parameters:
    - airport (str): The airport code for the arrival airport.
    - airports (dict): A dictionary containing airport codes as keys.

    Returns:
    - np.array: A NumPy array with 1 at the index corresponding to the arrival airport.
    """
    temp = np.zeros(len(airports))
    if airport in airports:
        temp[airports.get(airport)] = 1
        temp = temp.T
        return temp
    else:
        return None

# Load the model (finalized_model.pkl should be in the same directory)
def load_model():
    try:
        with open("finalized_model.pkl", "rb") as model_file:
            model = pickle.load(model_file)
        return model
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model file not found.")

# Function to filter and load data based on departure and arrival airports and times
def load_and_filter_data(departure_airport: str, arrival_airport: str, departure_time: datetime.datetime, arrival_time: datetime.datetime):
    filtered_data = []
    try:
        # Simulate loading data from a dataset (for demo, let's assume we use a static list of flights)
        with open('flights_data.json', 'r') as file:  # Assuming data is in 'flights_data.json'
            for line in file:
                flight_data = json.loads(line.strip())  # Each line is a separate JSON object

                # Filter by departure and arrival airports
                if flight_data["ORIGIN"] == departure_airport and flight_data["DEST"] == arrival_airport:
                    # Create datetime objects for the flight's departure and arrival times
                    flight_departure_time = datetime.datetime(year=flight_data["YEAR"], 
                                                              month=flight_data["MONTH"], 
                                                              day=flight_data["DAY_OF_MONTH"], 
                                                              hour=flight_data["CRS_DEP_TIME"] // 100, 
                                                              minute=flight_data["CRS_DEP_TIME"] % 100)
                    flight_arrival_time = datetime.datetime(year=flight_data["YEAR"], 
                                                            month=flight_data["MONTH"], 
                                                            day=flight_data["DAY_OF_MONTH"], 
                                                            hour=flight_data["CRS_ARR_TIME"] // 100, 
                                                            minute=flight_data["CRS_ARR_TIME"] % 100)
                    
                    # Filter by departure and arrival times (allowing for a 15-minute tolerance)
                    if abs((flight_departure_time - departure_time).total_seconds()) <= 900 and \
                       abs((flight_arrival_time - arrival_time).total_seconds()) <= 900:
                        filtered_data.append(flight_data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dataset file not found.")
    
    return filtered_data

# Function to calculate the average departure delay
def calculate_average_delay(filtered_data):
    if not filtered_data:
        raise HTTPException(status_code=404, detail="No data found for the specified parameters.")
    
    total_delay = 0
    for flight in filtered_data:
        total_delay += flight["DEP_DELAY"]
    
    average_delay = total_delay / len(filtered_data)
    return average_delay

# Prediction endpoint for delays
@app.get("/predict/delays")
def predict_delays(
    departure_airport: str,
    arrival_airport: str,
    departure_time: str,
    arrival_time: str
):
    
    print(f"Received request: {departure_airport}, {arrival_airport}, {departure_time}, {arrival_time}")
    """
    Predict the average departure delay based on the provided inputs.
    
    Parameters:
    - departure_airport (str): The code for the departure airport.
    - arrival_airport (str): The code for the arrival airport.
    - departure_time (str): The departure time in 'YYYY-MM-DD HH:MM:SS' format.
    - arrival_time (str): The arrival time in 'YYYY-MM-DD HH:MM:SS' format.
    
    Returns:
    - prediction (dict): A dictionary containing the predicted average departure delay in minutes.
    """
    # Convert the input times to datetime objects
    try:
        departure_time = datetime.datetime.strptime(departure_time, '%Y-%m-%d %H:%M:%S')
        arrival_time = datetime.datetime.strptime(arrival_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")
    
    # Simulate delay prediction logic for now
    return {"average_departure_delay_minutes": 15.0}

    # Load and filter data based on the request parameters
    filtered_data = load_and_filter_data(departure_airport, arrival_airport, departure_time, arrival_time)
    
    # Calculate the average departure delay
    average_delay = calculate_average_delay(filtered_data)
    
    # Return the average delay as a JSON response
    return {"average_departure_delay_minutes": average_delay}

# Endpoint to confirm the API is functional
@app.get("/")
def read_root():
    return {"message": "API is functional"}
