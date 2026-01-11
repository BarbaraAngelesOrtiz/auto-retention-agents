# test_batch_random.py
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import random

from agents.decision_agent import decide_action
from agents.action_agent import execute_action

CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"
BATCH_SIZE = 5  # cuántos clientes probar por corrida

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

        # Simulamos churn_score random si no existe
        churn_score = round(random.random(), 2)

        # Decidimos acción aleatoria
        action = decide_action(churn_score, mode="random")

        # Ejecutamos la acción real (Meet, Email, Sheets, Telegram)
        result = execute_action(
            action=action,
            customer_id=row_dict["customer_id"],
            churn_score=churn_score,
            row_data=row_dict
        )

        # Guardamos info resumida
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
