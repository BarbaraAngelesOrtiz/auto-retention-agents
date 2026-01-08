# agents/action_agent.py
from agents.ms_graph_agent import schedule_meeting
from agents.telegram_agent import send_telegram_message
from datetime import datetime, timedelta

USE_REAL_SERVICES = True  # Cambiar a False para seguir usando mocks

def execute_action(action: str, customer_id: str, churn_score: float = None) -> dict:
    if action == "send_email":
        if USE_REAL_SERVICES:
            return {"status": "email sent via Microsoft Graph", "customer": customer_id}
        else:
            return {"status": "email sent (mock)", "customer": customer_id}

    elif action == "schedule_meeting":
        if USE_REAL_SERVICES:
            start = (datetime.utcnow() + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")
            end = (datetime.utcnow() + timedelta(hours=24, minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")
            attendees = ["test@example.com"]  # reemplazar con emails reales
            return schedule_meeting(
                subject=f"Retention meeting: {customer_id}",
                start=start,
                end=end,
                attendees=attendees
            )
        else:
            return {"status": "meeting scheduled (mock)", "customer": customer_id}

    elif action == "send_telegram":
        if USE_REAL_SERVICES:
            text = f"Cliente {customer_id} tiene churn alto: {churn_score}"
            return send_telegram_message(text)
        else:
            return {"status": "telegram message sent (mock)", "customer": customer_id}

    else:
        return {"status": "no action required", "customer": customer_id}
