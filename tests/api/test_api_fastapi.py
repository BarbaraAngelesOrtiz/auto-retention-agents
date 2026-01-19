from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_healthcheck():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_run_customer():
    payload = {
        "customer_id": "TEST_001",
        "churn_prob": 0.72,
        "days_since_last_purchase": 420,
        "avg_purchase_value": 250,
        "income_bracket_Low": 1,
        "promo_flag": 1,
        "avg_discount_used": 0.35
    }

    r = client.post("/run-customer/", json=payload)
    assert r.status_code == 200

    data = r.json()
    assert data["customer_id"] == "TEST_001"
    assert "decision" in data
    assert "urgency" in data
