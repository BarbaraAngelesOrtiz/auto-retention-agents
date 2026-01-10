import os
import math
import base64

import pandas as pd
from dotenv import load_dotenv

from agents.action_agent import execute_action
from agents.decision_agent import decide_action

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# CONFIG
# =========================
CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"   # ajustá si el nombre es distinto
# Leer cliente de prueba (primer fila)
df = pd.read_csv(CSV_PATH)
TEST_CUSTOMER_ROW = df.iloc[0].to_dict()
TEST_CUSTOMER_ID = TEST_CUSTOMER_ROW["customer_id"]

# Función simple de simulación de churn
def simulate_churn(row):
    # Podés cambiar la lógica como quieras
    churn_value = 0.5
    if row.get("loyalty_program") == "No":
        churn_value += 0.2
    if row.get("days_since_last_purchase", 0) > 180:
        churn_value += 0.2
    return min(churn_value, 1.0)

# Función simple de decisión de acción según churn
def decide_action(churn_score):
    if churn_score >= 0.8:
        return "schedule_meeting"
    elif churn_score >= 0.5:
        return "send_email"
    elif churn_score >= 0.3:
        return "send_telegram"
    else:
        return "write_to_sheet"

# --- TEST CUSTOMER ---
print("=== TEST CUSTOMER ===")
print(f"ID: {TEST_CUSTOMER_ID}")
print(f"Data: {TEST_CUSTOMER_ROW}")

# Simular churn
churn_score = round(simulate_churn(TEST_CUSTOMER_ROW), 2)
print(f"\nSimulated Churn Score: {churn_score}")

# Decidir acción
action = decide_action(churn_score)
print(f"\nDecided Action: {action}")

# Ejecutar acción
print("\n=== EXECUTE ACTION ===")
result = execute_action(action, TEST_CUSTOMER_ID, churn_score=churn_score, row_data=TEST_CUSTOMER_ROW)
print(f"Result: {result}")

# Probar que se escriba también en Google Sheets
print("\n=== WRITE TO SHEET ===")
sheet_result = execute_action("write_to_sheet", TEST_CUSTOMER_ID, churn_score=churn_score, row_data=TEST_CUSTOMER_ROW)
print(f"Sheet Result: {sheet_result}")