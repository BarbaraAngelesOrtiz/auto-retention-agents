# tests/batch/test_batch_agents.py
from dotenv import load_dotenv
load_dotenv()

import pandas as pd

from agents.decision_agent import decide_action, batch_decisions
from agents.action_agent import execute_action

CSV_PATH = "data/customers_with_churn_prob.csv"
BATCH_SIZE = 5  # number of customers to test

print("\n RUNNING BATCH AGENT TEST \n")

# Upload test clients
df = pd.read_csv(CSV_PATH).head(BATCH_SIZE)

# Normalize columns for decision
def normalize_row(row):
    row_dict = row.to_dict()

    # Ensure that avg_purchase_value exists
    if "avg_purchase_value" not in row_dict:
        row_dict["avg_purchase_value"] = row_dict.get("total_sales", 0) / max(1, row_dict.get("purchase_frequency", 1))

    # Income_bracket flags
    for level in ["Low", "Medium", "High"]:
        key = f"income_bracket_{level}"
        if key not in row_dict:
            row_dict[key] = 1 if row_dict.get("income_bracket", "").lower() == level.lower() else 0

    # promo_flag
    if "promo_flag" not in row_dict:
        row_dict["promo_flag"] = 1 if row_dict.get("avg_discount_used", 0) > 0.3 else 0
    return row_dict

results = []

for i, row in df.iterrows():
    row_dict = normalize_row(row)
    customer_id = row_dict.get("customer_id", f"C{i+1}")
    row_dict["customer_id"] = customer_id

    print("-" * 40)
    print(f"Customer {customer_id}")

    # Decide on action
    try:
        decision = decide_action(row_dict)
        print(f"Decided action: {decision}")
    except Exception as e:
        print("❌ Error decidiendo acción:", e)
        decision = {
            "customer_id": customer_id,
            "decision_type": "NO_ACTION",
            "action_suggestion": "no_action",
            "urgency": "LOW",
            "value": row_dict.get("avg_purchase_value", "UNKNOWN"),
            "flags": [],
            "churn_prob": 0
        }

    # Execute action
    action_to_execute = decision.get("action_suggestion", "no_action")
    if action_to_execute != "no_action":
        try:
            result = execute_action(
                action=action_to_execute,
                customer_id=customer_id,
                churn_score=decision.get("churn_prob", 0),
                row_data=row_dict
            )
            print("Action result:", result)
        except Exception as e:
            print("❌ Error executing action:", e)
            result = {"status": "error", "error": str(e)}
    else:
        print("No action taken")
        result = {"status": "skipped"}

    results.append({
        "customer_id": customer_id,
        "churn_score": decision.get("churn_prob", 0),
        "action": action_to_execute,
        "result": result
    })

print("\n TEST SUMMARY \n")
for r in results:
    print(r)
