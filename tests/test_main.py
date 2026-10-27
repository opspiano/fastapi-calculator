from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Calculator" in response.text

def test_calculate_api_success():
    ops = [
        ("add", 10, 5, 15),
        ("subtract", 10, 4, 6),
        ("multiply", 3, 5, 15),
        ("divide", 20, 4, 5)
    ]
    for op, n1, n2, expected in ops:
        res = client.post("/calculate", json={"num1": n1, "num2": n2, "operation": op})
        assert res.status_code == 200
        assert res.json()["result"] == expected

def test_calculate_api_zero_division():
    res = client.post("/calculate", json={"num1": 10, "num2": 0, "operation": "divide"})
    assert res.status_code == 400
    assert "Cannot divide by zero" in res.json()["detail"]

def test_calculate_api_invalid_operation():
    res = client.post("/calculate", json={"num1": 10, "num2": 2, "operation": "modulo"})
    assert res.status_code == 400
