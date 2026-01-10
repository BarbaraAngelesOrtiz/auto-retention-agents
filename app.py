from fastapi import FastAPI
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

from agents.action_agent import execute_action

# Dataset de ejemplo
DATA_PATH = os.path.join("data", "Grocery_Customer_Churn_Data_Augmented.csv")
df = pd.read_csv(DATA_PATH, dtype={"customer_id": str})

app = FastAPI(title="AutoRetention Agents - Google")

@app.get("/")
def root():
    return {"status": "AutoRetention Agents running"}

@app.get("/customer_ids")
def customer_ids():
    return df["customer_id"].dropna().tolist()[:20]

@app.get("/simulate_decision/{customer_id}")
def simulate_decision(customer_id: str):
    row = df[df["customer_id"] == customer_id]
    if row.empty:
        return {"error": f"Customer ID {customer_id} not found"}

    customer = row.iloc[0].to_dict()
    churn_score = round(customer.get("churn_score", 0.5), 2)  # ejemplo simple

    # Aquí definimos las acciones a ejecutar
    actions = ["send_email", "schedule_meeting", "log_sheet", "send_chat"]
    results = {a: execute_action(a, customer_id, churn_score) for a in actions}

    return {
        "customer_id": customer_id,
        "churn_score": churn_score,
        "results": results
    }
