# test_api.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"


# UTIL
def pretty(resp):
    try:
        return json.dumps(resp.json(), indent=2)
    except Exception:
        return resp.text


# TESTS 
def test_healthcheck():
    resp = requests.get(f"{BASE_URL}/")
    print("=== HEALTHCHECK ===")
    print(resp.status_code)
    print(pretty(resp))
    print()


def test_run_customer():
    """
    Test end-to-end:
    input customer → churn model → decision agent → action agent
    """

    customer_payload = {
        "customer_id": "TEST_001",
        "days_since_last_purchase": 420,
        "total_sales": 820,
        "income_bracket": "Low",
        "purchase_frequency": 5,
        "avg_discount_used": 0.35
    }

    resp = requests.post(
        f"{BASE_URL}/run-customer",
        json=customer_payload
    )

    print("=== RUN SINGLE CUSTOMER ===")
    print(resp.status_code)
    print(pretty(resp))
    print()


def test_run_batch():
    """
    Batch test with multiple customers.
    Manager should receive only summary (handled server-side).
    """

    batch_payload = {
        "customers": [
            {
                "customer_id": "BATCH_001",
                "days_since_last_purchase": 500,
                "total_sales": 1200,
                "income_bracket": "Low",
                "purchase_frequency": 6,
                "avg_discount_used": 0.4
            },
            {
                "customer_id": "BATCH_002",
                "days_since_last_purchase": 30,
                "total_sales": 150,
                "income_bracket": "High",
                "purchase_frequency": 1,
                "avg_discount_used": 0.05
            },
            {
                "customer_id": "BATCH_003",
                "days_since_last_purchase": 200,
                "total_sales": 600,
                "income_bracket": "Medium",
                "purchase_frequency": 4,
                "avg_discount_used": 0.25
            }
        ]
    }

    resp = requests.post(
        f"{BASE_URL}/run-batch",
        json=batch_payload
    )

    print("=== RUN BATCH ===")
    print(resp.status_code)
    print(pretty(resp))
    print()

    if resp.ok:
        summary = resp.json().get("manager_summary", {})
        print("=== MANAGER SUMMARY ===")
        print(json.dumps(summary, indent=2))
        print()


# MAIN 
if __name__ == "__main__":
    test_healthcheck()
    test_run_customer()
    test_run_batch()
