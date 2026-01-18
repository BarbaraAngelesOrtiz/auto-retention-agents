# tests/batch/test_batch_agents.py
from dotenv import load_dotenv
load_dotenv()

import pandas as pd

from agents.decision_agent import decide_action
from agents.action_agent import execute_action

CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"
BATCH_SIZE = 5  # número de clientes a testear

print("\n=== RUNNING BATCH AGENT TEST ===\n")

# Cargar clientes de prueba
df = pd.read_csv(CSV_PATH).head(BATCH_SIZE)

results = []

for i, row in df.iterrows():
    row_dict = row.to_dict()
    customer_id = row_dict.get("CustomerID", f"C{i}")

    print("-" * 40)
    print(f"Customer {customer_id}")

    # 1️⃣ Calcular churn probability
    try:
        churn_prob = predict_churn(row_dict)
        print(f"Churn probability: {churn_prob}")
    except Exception as e:
        print("❌ Error calculando churn:", e)
        churn_prob = 0

    # 2️⃣ Calcular flags
    flags = assign_flags(row_dict, churn_prob)
    print("Flags:", flags)

    # 3️⃣ Decidir acción
    try:
        action = decide_action(customer_data=row_dict, churn_prob=churn_prob)
        print(f"Decided action: {action}")
    except Exception as e:
        print("❌ Error decidiendo acción:", e)
        action = "no_action"

    # 4️⃣ Ejecutar acción
    if action != "no_action":
        try:
            result = execute_action(
                action=action,
                customer_id=customer_id,
                churn_score=churn_prob,
                row_data=row_dict
            )
            print("Action result:", result)
        except Exception as e:
            print("❌ Error ejecutando acción:", e)
            result = {"status": "error", "error": str(e)}
    else:
        print("No action taken")
        result = {"status": "skipped"}

    results.append({
        "customer_id": customer_id,
        "churn_score": churn_prob,
        "action": action,
        "result": result
    })

print("\n=== TEST SUMMARY ===\n")
for r in results:
    print(r)
