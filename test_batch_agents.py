# test_batch_agents.py
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import numpy as np

from agents.scoring_agent import calculate_churn_score # tu función que genera probabilidades
from agents.decision_agent import decide_action
from agents.action_agent import execute_action

CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"
BATCH_SIZE = 5  # cantidad de clientes a testear

# 1️⃣ Cargar clientes
df = pd.read_csv(CSV_PATH).head(BATCH_SIZE)

results = []

for _, row in df.iterrows():
    customer_id = row["customer_id"]

    # 2️⃣ Simular churn_score si no lo tenés
    churn_score = calculate_churn_score(row)  # devuelve un float entre 0 y 1
    churn_score = round(churn_score, 2)

    # 3️⃣ Decidir acción
    action = decide_action(churn_score)

    # 4️⃣ Ejecutar acción (email, meet, telegram, sheet)
    result = execute_action(
        action=action,
        customer_id=customer_id,
        churn_score=churn_score,
        row_data=row.to_dict()
    )

    results.append({
        "customer_id": customer_id,
        "churn_score": churn_score,
        "action": action,
        "result": result
    })

# 5️⃣ Mostrar resultados
for r in results:
    print(r)
