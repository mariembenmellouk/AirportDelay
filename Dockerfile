# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Expose the port 
EXPOSE 5000

# Command to run the application using uvicorn
CMD ["uvicorn", "API_Version2:app", "--host", "0.0.0.0", "--port", "5000"]


