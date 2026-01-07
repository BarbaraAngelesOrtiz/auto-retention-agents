from fastapi import FastAPI
from agents.decision_agent import decide_action
from agents.action_agent import execute_action
from utils.churn_simulator import simulate_churn
import pandas as pd

# Cargar dataset
df = pd.read_csv("data/Grocery_Customer_Churn_Data_Augmented.csv", dtype={"customer_id": str})

app = FastAPI(title="AutoRetention Agents")

@app.get("/test")
def test_endpoint():
    return {"status": "simulate_decision exists!"}

@app.get("/")
def root():
    return {"status": "AutoRetention Agents is running"}

@app.get("/simulate_decision/{customer_id}")
def simulate_decision(customer_id: str):
    # Buscar cliente
    row = df[df["customer_id"] == customer_id]
    if row.empty:
        return {"error": f"Customer ID {customer_id} not found"}

    customer = row.iloc[0].to_dict()

    # Simular churn
    churn_score = simulate_churn(customer)

    # Customer value
    customer_value = customer.get("total_sales", 1000)
    customer_name = customer.get("customer_id", customer_id)

    # Agentes
    action = decide_action(churn_score, customer_value)
    result = execute_action(action, customer_name)

    return {
        "customer_id": customer_id,
        "churn_score": churn_score,
        "action": action,
        "result": result
    }
