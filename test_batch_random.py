# test_batch_random.py
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import random

from agents.decision_agent import decide_action
from agents.action_agent import execute_action

CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"
BATCH_SIZE = 5  

def clean_row(row: dict) -> dict:
    """Limpia NaN para evitar errores en Sheets / JSON"""
    clean = {}
    for k, v in row.items():
        clean[k] = "" if pd.isna(v) else v
    return clean

def run_batch_random(limit=BATCH_SIZE):
    df = pd.read_csv(CSV_PATH).head(limit)
    results = []

    for _, row in df.iterrows():
        row_dict = clean_row(row.to_dict())

        # Random churn_score simulation if it does not exist
        churn_score = round(random.random(), 2)

        # Random action decision
        action = decide_action(churn_score, mode="random")

        # Execution of the real action (Meet, Email, Sheets, Telegram)
        result = execute_action(
            action=action,
            customer_id=row_dict["customer_id"],
            churn_score=churn_score,
            row_data=row_dict
        )

        # We saved summary information
        results.append({
            "customer_id": row_dict["customer_id"],
            "churn_score": churn_score,
            "action": action,
            "status": result.get("status"),
            "extra": {k: v for k, v in result.items() if k not in ["status"]}
        })

    return results

if __name__ == "__main__":
    batch_results = run_batch_random()
    print("=== BATCH RANDOM RESULTS ===")
    for r in batch_results:
        print(
            f"Customer {r['customer_id']}: churn={r['churn_score']}, "
            f"action={r['action']}, status={r['status']}, extra={r['extra']}"
        )
