from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Transaction System!"}

def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "John Doe", "pin": "1234", "budget": 5000.0, "tier": "basic"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["tier"] == "basic"

def test_create_transaction():
    # First, create a user
    user_response = client.post(
        "/users/",
        json={"name": "Jane Doe", "pin": "5678", "budget": 5000.0, "tier": "basic"}
    )
    user_id = user_response.json()["id"]

    # Create a money transfer transaction
    response = client.post(
        "/transactions/",
        json={
            "type": "money_transfer",
            "pin": "5678",
            "details": {
                "payee_name": "Alice",
                "amount": 1000.0,
                "remarks": "Test transfer"
            }
        },
        headers={"X-User-ID": str(user_id)}
    )
    assert response.status_code == 200
    assert response.json()["type"] == "money_transfer"
    assert response.json()["amount"] == 1000.0