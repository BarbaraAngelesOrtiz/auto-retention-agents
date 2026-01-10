# agents/action_agent.py
import os
from dotenv import load_dotenv
load_dotenv() 
from datetime import datetime, timedelta
import re

# Import de agentes
from agents.google_calendar_agent import create_event as create_calendar_event
from agents.gmail_agent import send_email
from agents.google_sheets_agent import write_to_sheet
from agents.telegram_agent import send_telegram_message, telegram_enabled

USE_REAL_SERVICES = True  # False = mocks

# Función para escapar caracteres especiales de Telegram MarkdownV2
def escape_telegram_text(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def execute_action(action: str, customer_id: str, churn_score: float = None, row_data=None) -> dict:
    """
    Ejecuta una acción sobre el cliente:
    - send_email
    - schedule_meeting
    - send_telegram
    - write_to_sheet
    """

    if action == "send_email":
        if USE_REAL_SERVICES:
            subject = f"Atencion cliente {customer_id}"
            body = f"Estimado equipo, el cliente {customer_id} tiene churn score {churn_score}."
            result = send_email(subject, body)
            return {"status": "email sent", "result": result}
        else:
            return {"status": "email sent (mock)", "customer": customer_id}

    elif action == "schedule_meeting":
        start = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
        end = (datetime.utcnow() + timedelta(hours=25)).isoformat() + "Z"
        attendees = [os.getenv("GMAIL_RECIPIENT")] if os.getenv("GMAIL_RECIPIENT") else []
        if USE_REAL_SERVICES:
            event = create_calendar_event(
                summary=f"Retention meeting: {customer_id}",
                description=f"Evento generado automáticamente para retención del cliente {customer_id}",
                start=start,
                end=end,
                attendees=attendees
            )
            return {"status": "calendar event created", "event": event}
        else:
            return {"status": "calendar event created (mock)", "customer": customer_id}
        
    elif action == "send_telegram":
        text = f"🚨 Cliente {customer_id} con churn alto ({churn_score})"
        text = escape_telegram_text(text)  # <-- escapamos caracteres especiales
        if USE_REAL_SERVICES and telegram_enabled():
            result = send_telegram_message(text)
            return {"status": "telegram message sent", "result": result}
        else:
            return {"status": "telegram message sent (mock)", "customer": customer_id}

    elif action == "write_to_sheet":
        if USE_REAL_SERVICES and row_data:
     
            values = [list(row_data.keys()), list(row_data.values())]
            
            result = write_to_sheet("Sheet1!A1", values)

            return {"status": "sheet updated", "result": result}
        else:
            return {"status": "sheet updated (mock)", "customer": customer_id}

