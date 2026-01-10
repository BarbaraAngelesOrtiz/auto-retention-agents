# test_agents.py
import os
import numpy as np
from agents.action_agent import execute_action

# ==== TEST CUSTOMER ====
TEST_CUSTOMER_ID = "C1000"
TEST_CUSTOMER_ROW = {
    "customer_id": "C1000",
    "age": 33,
    "gender": "Other",
    "income_bracket": "Medium",
    "loyalty_program": "Yes",
    "membership_years": 1,
    "marital_status": "Divorced",
    "number_of_children": 2,
    "education_level": "Master's",
    "occupation": "Retired",
    "transaction_id": "T1000",
    "transaction_date": "2023-01-01",
    "product_category": "Electronics",
    "quantity": 1,
    "unit_price": 75.45668142001342,
    "avg_purchase_value": np.nan,
    "purchase_frequency": np.nan,
    "last_purchase_date": "2023-01-01",
    "avg_discount_used": 11.33685322284007,
    "online_purchases": 6,
    "in_store_purchases": 0,
    "total_sales": 1563.705816815419,
    "total_transactions": 41,
    "total_items_purchased": 55,
    "promotion_type": np.nan,
    "promotion_effectiveness": "Medium",
    "days_since_last_purchase": 181,
    "churn": 0,
}

# ==== DECIDE ACTION SIMULADO ====
# Aquí simulamos un churn score para decidir acción
churn_score = 0.9  # por ejemplo
if churn_score > 0.8:
    action = "schedule_meeting"
elif churn_score > 0.5:
    action = "send_email"
else:
    action = "write_to_sheet"  # o "send_telegram"
    
print("=== TEST CUSTOMER ===")
print(f"ID: {TEST_CUSTOMER_ID}")
print(f"Data: {TEST_CUSTOMER_ROW}\n")

print(f"Simulated Churn Score: {churn_score}")
print(f"Decided Action: {action}\n")

# ==== EXECUTE MAIN ACTION ====
result = execute_action(action, TEST_CUSTOMER_ID, churn_score=churn_score, row_data=TEST_CUSTOMER_ROW)
print("=== EXECUTE ACTION ===")
print("Result:", result, "\n")

# ==== WRITE TO SHEET ====
# Siempre limpiar NaN/None antes de enviar
def clean_row(row):
    return ["" if (v is None or (isinstance(v, float) and np.isnan(v))) else v for v in row]

values = [list(TEST_CUSTOMER_ROW.keys()), clean_row(list(TEST_CUSTOMER_ROW.values()))]

sheet_result = execute_action("write_to_sheet", TEST_CUSTOMER_ID, churn_score=churn_score, row_data=TEST_CUSTOMER_ROW)
print("=== WRITE TO SHEET ===")
print(sheet_result, "\n")

# ==== SEND EMAIL ====
email_result = execute_action("send_email", TEST_CUSTOMER_ID, churn_score=churn_score)
print("=== SEND EMAIL ===")
print(email_result, "\n")

# ==== SEND TELEGRAM ====
telegram_result = execute_action("send_telegram", TEST_CUSTOMER_ID, churn_score=churn_score)
print("=== SEND TELEGRAM ===")
print(telegram_result, "\n")
