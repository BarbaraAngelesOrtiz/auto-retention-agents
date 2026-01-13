# test_batch_agents.py
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import numpy as np

from agents.scoring_agent import calculate_churn_score 
from agents.decision_agent import decide_action
from agents.action_agent import execute_action

CSV_PATH = "data/Grocery_Customer_Churn_Data_Augmented.csv"
BATCH_SIZE = 5  # number of customers to test

# Data ingestion
df = pd.read_csv(CSV_PATH).head(BATCH_SIZE)

results = []

for _, row in df.iterrows():
    customer_id = row["customer_id"]

    # Simulate churn_score 
    churn_score = calculate_churn_score(row)  # returns a float between 0 and 1
    churn_score = round(churn_score, 2)

    # Decide on action
    action = decide_action(churn_score)

    # Execute action (email, meet, telegram, sheet)
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

# Show results
for r in results:
    print(r)
