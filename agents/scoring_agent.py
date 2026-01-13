# agents/scoring_agent.py
import os
from dotenv import load_dotenv

from utils.churn_simulator import simulate_churn

def calculate_churn_score(customer_row: dict) -> float:
    """
    Churn simulator wrapper.
    This may be replaced with a real ML model in the future.
    """
    return simulate_churn(customer_row)
