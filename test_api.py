# test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_healthcheck():
    resp = requests.get(f"{BASE_URL}/")
    print("=== HEALTHCHECK ===")
    print(resp.status_code, resp.json())
    print()

def test_sample_customer():
    resp = requests.get(f"{BASE_URL}/customers/sample")
    print("=== SAMPLE CUSTOMER ===")
    print(resp.status_code, resp.json())
    print()

def test_run_customer(customer_id="C0"):
    resp = requests.post(f"{BASE_URL}/run-customer/{customer_id}")
    print(f"=== RUN CUSTOMER {customer_id} ===")
    print(resp.status_code, resp.json())
    print()

def test_run_batch(limit=5):
    resp = requests.post(f"{BASE_URL}/run-batch?limit={limit}")
    print(f"=== RUN BATCH (limit={limit}) ===")
    print(resp.status_code, resp.json())
    print()

def test_run_batch_real():
    print("\n=== RUN BATCH REAL (limit=3) ===")
    payload = {"limit": 3}  # los primeros 3 clientes
    resp = requests.post(f"{BASE_URL}/run-batch", params=payload)
    print(resp.status_code, resp.json())

    # Mostrar detalles de cada cliente procesado
    results = resp.json().get("results", [])
    for r in results:
        print(f"Cliente {r['customer_id']}: churn_score={r['churn_score']}, "
              f"acción={r['action']}, status={r['status']}")

if __name__ == "__main__":
    test_healthcheck()
    test_sample_customer()
    test_run_customer("C0")  # Replace with a valid customer_id from the CSV
    test_run_batch(3)        # We tested a batch of 3 customers
    test_run_batch_real()

