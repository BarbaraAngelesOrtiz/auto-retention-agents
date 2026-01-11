# app.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import pandas as pd
from typing import Dict, Any

from agents.decision_agent import decide_action
from agents.action_agent import execute_action

CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"

app = FastAPI(
    title="Auto Retention Agents API",
    description="Sistema multi-agente para churn y retención",
    version="1.0"
)


def clean_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Limpia NaN para evitar errores en Sheets / JSON
    """
    clean = {}
    for k, v in row.items():
        if pd.isna(v):
            clean[k] = ""
        else:
            clean[k] = v
    return clean


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.get("/customers/sample")
def sample_customer():
    df = pd.read_csv(CSV_PATH)
    row = clean_row(df.iloc[0].to_dict())
    return row


@app.post("/run-customer/{customer_id}")
def run_customer(customer_id: str):
    df = pd.read_csv(CSV_PATH)

    customer = df[df["customer_id"] == customer_id]
    if customer.empty:
        return {"error": "Customer not found"}

    row = clean_row(customer.iloc[0].to_dict())

    churn_value = float(row.get("churn", 0))
    churn_score = round(churn_value, 2)

    action = decide_action(churn_score)

    result = execute_action(
        action=action,
        customer_id=customer_id,
        churn_score=churn_score,
        row_data=row
    )

    return {
        "customer_id": customer_id,
        "churn_score": churn_score,
        "action": action,
        "result": result
    }


@app.post("/run-batch")
def run_batch(limit: int = 10):
    df = pd.read_csv(CSV_PATH).head(limit)

    results = []

    for _, row in df.iterrows():
        row_dict = clean_row(row.to_dict())

        churn_score = float(row_dict.get("churn", 0))
        action = decide_action(churn_score)

        result = execute_action(
            action=action,
            customer_id=row_dict["customer_id"],
            churn_score=churn_score,
            row_data=row_dict
        )

        results.append({
            "customer_id": row_dict["customer_id"],
            "churn_score": churn_score,
            "action": action,
            "status": result["status"]
        })

    return {
        "processed": len(results),
        "results": results
    }

