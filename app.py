# app.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from typing import Dict, Any, List
import pandas as pd

from agents.decision_agent import decide_action, batch_decisions
from agents.action_agent import execute_actions

# FASTAPI
app = FastAPI(
    title="Auto Retention Agents API",
    description="Multi-agent system for churn and retention",
    version="1.0"
)

# UTILS
def clean_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Clean NaN to avoid errors in Sheets/JSON"""
    return {k: "" if pd.isna(v) else v for k, v in row.items()}

# HEALTHCHECK
@app.get("/")
def healthcheck():
    return {"status": "ok"}

# SAMPLE CUSTOMER
@app.get("/customers/sample")
def sample_customer():
    CSV_PATH = "data/customers_with_churn_prob.csv"
    df = pd.read_csv(CSV_PATH)
    row = clean_row(df.iloc[0].to_dict())
    return row

# RUN SINGLE CUSTOMER
@app.post("/run-customer/")
def run_customer(customer_data: Dict[str, Any]):
    """
    Run the churn and retention flow for a single customer.
    """
    row = clean_row(customer_data)

    # Decision
    decision = decide_action(row)

    # Execute action
    action_result = execute_actions([decision])

    return {
        "customer_id": row.get("customer_id"),
        "churn_prob": decision.get("churn_prob"),
        "value": decision.get("value"),
        "flags": decision.get("flags"),
        "decision": decision.get("action_suggestion"),
        "urgency": decision.get("urgency"),
        "action_result": action_result
    }

# RUN BATCH
@app.post("/run-batch/")
def run_batch(customers: List[Dict[str, Any]]):
    """
    Execute the workflow for a batch of customers.
    """
    cleaned_customers = [clean_row(c) for c in customers]

    # Batch decisions
    batch_result = batch_decisions(cleaned_customers)
    customer_actions = batch_result["customer_actions"]

    # Execute all actions
    results = execute_actions(customer_actions)

    return {
        "processed_customers": len(cleaned_customers),
        "customer_actions": customer_actions,
        "manager_summary": batch_result["manager_summary"],
        "results": results
    }
