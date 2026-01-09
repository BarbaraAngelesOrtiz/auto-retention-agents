# app.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import pandas as pd
import os

from utils.churn_simulator import simulate_churn
from agents.decision_agent import decide_action
from agents.action_agent import execute_action
from agents.ms_graph_agent import ms_graph_healthcheck


# ======== Cargar dataset ========
DATA_PATH = os.path.join("data", "Grocery_Customer_Churn_Data_Augmented.csv")
df = pd.read_csv(DATA_PATH, dtype={"customer_id": str})

# ======== Inicializar FastAPI ========
app = FastAPI(title="AutoRetention Agents")

# ======== Endpoint raíz ========
@app.get("/")
def root():
    return {"status": "AutoRetention Agents is running"}

# ======== Endpoint para ver primeros customer_ids ========
@app.get("/customer_ids")
def customer_ids():
    return df["customer_id"].dropna().tolist()[:20]

# ======== Endpoint de simulación de decisión con agentes ========
@app.get("/simulate_decision/{customer_id}")
def simulate_decision(customer_id: str):
    # Buscar cliente en dataset
    row = df[df["customer_id"] == customer_id]
    if row.empty:
        return {"error": f"Customer ID {customer_id} not found"}

    customer = row.iloc[0].to_dict()

    # Simular churn
    churn_score = simulate_churn(customer)

    # ======== Usar agente de decisión ========
    action = decide_action(churn_score)

    # ======== Usar agente de acción ========
    result = execute_action(action, customer_id, churn_score=churn_score)

    return {
        "customer_id": customer_id,
        "churn_score": churn_score,
        "action": action,
        "result": result
    }

# ======== Endpoint de healthcheck para Microsoft Graph ========
@app.get("/health/ms-graph")
def health_ms_graph():
    return ms_graph_healthcheck()

