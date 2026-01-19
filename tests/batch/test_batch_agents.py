# tests/batch/test_batch_agents.py
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from agents.decision_agent import decide_action
from agents.action_agent import execute_actions

CSV_PATH = "data/customers_with_churn_prob.csv"
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
        action_data = decide_action(row_dict)
        print(f"Decided action: {action_data}")
    except Exception as e:
        print("❌ Error decidiendo acción:", e)
        action_data = {
            "customer_id": customer_id,
            "churn_prob": churn_prob,
            "decision_type": "NO_ACTION",
            "action_suggestion": "no_action",
            "urgency": "LOW",
            "value": "UNKNOWN",
            "flags": []
        }

    # 4️⃣ Ejecutar acción usando execute_actions
    try:
        exec_result = execute_actions([action_data])
        print("Action execution result:", exec_result)
    except Exception as e:
        print("❌ Error ejecutando acción:", e)
        exec_result = {"status": "error", "error": str(e)}

    results.append({
        "customer_id": customer_id,
        "churn_score": churn_prob,
        "action_data": action_data,
        "execution_result": exec_result
    })

print("\n=== TEST SUMMARY ===\n")
for r in results:
    print(r)
