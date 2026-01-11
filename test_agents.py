
from dotenv import load_dotenv
load_dotenv() 

import pandas as pd
from agents.decision_agent import decide_action
from agents.action_agent import execute_action
from agents.scoring_agent import calculate_churn_score

CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"
MAX_CUSTOMERS = 5    # para no spamear Calendar / Email
CHURN_THRESHOLD = 0.6


def run_system_test():
    print("\n=== START END-TO-END SYSTEM TEST ===\n")

    df = pd.read_csv(CSV_PATH)

    tested = 0

    for _, row in df.iterrows():
        if tested >= MAX_CUSTOMERS:
            break

        customer_id = row.get("CustomerID", f"C{tested}")
        print("-" * 40)
        print(f"Customer: {customer_id}")

        # 1️⃣ Calcular churn score
        row_dict = row.to_dict()
        churn_score = calculate_churn_score(row_dict)

        print(f"Churn score: {round(churn_score, 3)}")

        # 2️⃣ Decidir acción
        action = decide_action(churn_score)
        print(f"Decided action: {action}")

        # 3️⃣ Ejecutar acción
        if action != "no_action":
            try:
                result = execute_action(
                    action=action,
                    customer_id=customer_id,
                    churn_score=churn_score,
                    row_data=row.to_dict()
                )
                print("Action result:", result)
            except Exception as e:
                print("❌ ERROR executing action:", e)
        else:
            print("No action taken")

        tested += 1
        print()

    print("\n=== END SYSTEM TEST ===")


if __name__ == "__main__":
    run_system_test()
