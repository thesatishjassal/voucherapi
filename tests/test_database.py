
import pytest
from fastapi.testclient import TestClient
from app.main import app  # FastAPI app import
from sqlalchemy.orm import Session
from database import get_db_connection
import uuid

# Create the test client
client = TestClient(app)

@pytest.fixture
def test_db():
    db = get_db_connection()  
    yield db
    db.close()  

def test_create_user(test_db: Session):
    unique_phone = f"9989{uuid.uuid4().hex[:6]}"  
    response = client.post(
        "/users/", 
        json={"name": "John Doe", "phone": unique_phone, "password": "secret"}
    )
    assert response.status_code == 201
    response_data = response.json()
    assert "User added successfully" in response_data["message"]

# def test_create_user_duplicate_phone(test_db: Session):
#     unique_phone = f"9989{uuid.uuid4().hex[:6]}"  
#     client.post("/users/", json={"name": "John Doe", "phone": unique_phone, "password": "fdftrrgfg"})

#     response = client.post("/users/", json={"name": "Rakesh", "phone": unique_phone, "password": "fdfdftrtr"})
    
#     print("Response JSON:", response.json())  # Debugging

#     assert response.status_code == 400
#     assert "detail" in response.json(), "Error response is missing 'detail' key"
#     assert response.json()["detail"] == "Phone Number already exists!"

def test_get_all_users(test_db: Session):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure it's a list of users
