import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pandas as pd
from agents.decision_agent import decide_action, batch_decisions
from agents.action_agent import execute_actions

CSV_PATH = "data/customers_with_churn_prob.csv"
BATCH_SIZE = 5  # número de clientes a testear

print("\n=== RUNNING BATCH AGENT TEST ===\n")

# Cargar clientes de prueba
df = pd.read_csv(CSV_PATH).head(BATCH_SIZE)

results = []

for i, row in df.iterrows():
    row_dict = row.to_dict()
    customer_id = row_dict.get("customer_id", f"C{i}")

    print("-" * 40)
    print(f"Customer {customer_id}")

    # 1️⃣ Decidir acción
    try:
        action = decide_action(row_dict)
        print(f"Decided action: {action}")
    except Exception as e:
        print("❌ Error decidiendo acción:", e)
        action = {"action_suggestion": "no_action"}

    # 2️⃣ Ejecutar acción
    if action.get("action_suggestion") != "no_action":
        try:
            result = execute_actions([action])
            print("Action result:", result)
        except Exception as e:
            print("❌ Error ejecutando acción:", e)
            result = {"status": "error", "error": str(e)}
    else:
        print("No action taken")
        result = {"status": "skipped"}

    results.append({
        "customer_id": customer_id,
        "action": action,
        "result": result
    })

print("\n=== TEST SUMMARY ===\n")
for r in results:
    print(r)
