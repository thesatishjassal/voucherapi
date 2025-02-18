import pytest
from fastapi.testclient import TestClient
from app.main import app  # FastAPI app import
from sqlalchemy.orm import Session
from database import get_db_connection
import random


# Create the test client
client = TestClient(app)

def generate_unique_phone():
    unique_digits = random.randint(100000, 999999)  # Ensure a 6-digit number
    print("Unique digits:", unique_digits)  # Debugging
    return f"9989{unique_digits}"  # Prefix with '9989' to make it 10 digits

@pytest.fixture
def test_db():
    db = get_db_connection()  
    try:
        yield db
    finally:
        db.close()  # Ensure cleanup happens even if an error occurs during the test

def test_create_user(test_db: Session):
    unique_phone = generate_unique_phone()
    response = client.post(
        "/users/", 
        json={"name": "John Doe", "phone": unique_phone, "password": "pass"}
    )
    assert response.status_code == 201
    response_data = response.json()
    assert "User added successfully" in response_data["message"]

def test_create_user_duplicate_phone(test_db: Session):
    unique_phone = generate_unique_phone() 
    # First user creation
    client.post("/users/", json={"name": "John Doe", "phone": unique_phone, "password": "pass"})

    # Second attempt with duplicate phone
    response = client.post("/users/", json={"name": "Rakesh", "phone": unique_phone, "password": "pass"})
    
    print("Response JSON:", response.json())  # Debugging

    assert response.status_code == 400
    assert "message" in response.json(), "Error response is missing 'message' key"
    assert response.json()["message"] == "Phone Number already exists!"

def test_get_all_users(test_db: Session):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure it's a list of users
