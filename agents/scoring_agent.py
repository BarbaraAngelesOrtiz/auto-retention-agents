# agents/scoring_agent.py
import os
from dotenv import load_dotenv

from utils.churn_simulator import simulate_churn

def calculate_churn_score(customer_row: dict) -> float:
    """
    Wrapper del simulador de churn.
    En el futuro puede cambiarse por un modelo ML real.
    """
    return simulate_churn(customer_row)
