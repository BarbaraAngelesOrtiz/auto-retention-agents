# agents/action_agent.py

from agents.ms_graph_agent import create_calendar_event
from agents.telegram_agent import send_telegram_message
from datetime import datetime, timedelta

USE_REAL_SERVICES = True  # False = mocks

def execute_action(action: str, customer_id: str, churn_score: float = None) -> dict:

    if action == "send_email":
        # (lo dejamos preparado para después)
        return {
            "status": "email sent via Microsoft Graph" if USE_REAL_SERVICES else "email sent (mock)",
            "customer": customer_id
        }

    elif action == "schedule_meeting":
        if USE_REAL_SERVICES:
            start = (datetime.utcnow() + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")
            end = (datetime.utcnow() + timedelta(hours=24, minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")
            attendees = ["tu_correo@dominio.com"]  # reemplazar por un correo válido
            return create_calendar_event(
                subject=f"Retention meeting: {customer_id}",
                body="Evento generado automáticamente para retención",
                start=start,
                end=end
            )

    elif action == "send_telegram":

        text = f"🚨 Cliente {customer_id} con churn alto ({churn_score})"

        if USE_REAL_SERVICES:
            return send_telegram_message(text)
        else:
            return {"status": "telegram message sent (mock)", "customer": customer_id}

    else:
        return {"status": "no action required", "customer": customer_id}
    
res = create_calendar_event(
    subject="Prueba AutoRetention",
    body="Evento generado automáticamente desde FastAPI",
    start="2026-01-10T10:00:00",
    end="2026-01-10T10:30:00"
)

print(res)