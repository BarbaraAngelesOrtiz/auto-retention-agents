# app.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd

from agents.scoring_agent import predict_churn, assign_flags, compute_economic_value
from agents.decision_agent1 import decide_action, batch_decisions
from agents.action_agent import execute_action

# FASTAPI 
app = FastAPI(
    title="Auto Retention Agents API",
    description="Multi-agent system for churn and retention",
    version="1.0"
)

# UTILS 
def clean_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean NaN to avoid errors in Sheets/JSON
    """
    return {k: "" if pd.isna(v) else v for k, v in row.items()}

# HEALTHCHECK 
@app.get("/")
def healthcheck():
    return {"status": "ok"}

# SAMPLE CUSTOMER 
@app.get("/customers/sample")
def sample_customer():
    
    CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"
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

    # Churn prediction
    churn_prob = predict_churn(row)

    # Flags and economic value
    flags = assign_flags(row, churn_prob)
    econ_value = compute_economic_value(row)

    # Action decision
    decision = decide_action(row, churn_prob)

    # Action execution
    action_result = execute_action(
        action=decision["recommended_action"],
        customer_id=row["customer_id"],
        churn_score=churn_prob,
        row_data=row
    )

    # Return result for logging/UI
    return {
        "customer_id": row["customer_id"],
        "churn_prob": churn_prob,
        "flags": flags,
        "economic_value": econ_value,
        "decision": decision["recommended_action"],
        "followup_email": decision.get("followup_email"),
        "justification": decision.get("justification"),
        "action_result": action_result
    }

# RUN BATCH 
@app.post("/run-batch/")
def run_batch(customers: List[Dict[str, Any]]):
    """
    Execute the workflow for a batch of customers.
    Generate a consolidated summary for the manager.
    """
    # Clean data
    cleaned_customers = [clean_row(c) for c in customers]

    # Batch decisions
    batch_result = batch_decisions(cleaned_customers)
    customer_actions = batch_result["customer_actions"]
    manager_summary = batch_result["manager_summary"]

    # Execute actions per client
    for action_data in customer_actions:
        execute_action(
            action=action_data["recommended_action"],
            customer_id=action_data["customer_id"],
            churn_score=action_data["churn_prob"],
            row_data=action_data
        )

    # Return summary for manager
    return {
        "processed_customers": len(cleaned_customers),
        "customer_actions": customer_actions,
        "manager_summary": manager_summary
    }
