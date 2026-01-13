# agents/action_agent.py
import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

from agents.google_calendar_agent import create_event_with_meet
from agents.gmail_agent import send_email
from agents.google_sheets_agent import write_to_sheet, append_to_sheet 
from agents.telegram_agent import send_telegram_message, telegram_enabled

USE_REAL_SERVICES = True

# Util
def escape_telegram_text(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


# MAIN 
def execute_action(
    action: str,
    customer_id: str,
    churn_score: float,
    row_data: dict | None = None
) -> dict:

    # EMAIL
    if action == "send_email":
        subject = f"Customer service {customer_id}"
        body = f"Customer {customer_id} with churn score {churn_score}"

        if USE_REAL_SERVICES:
            result = send_email(subject, body)
            return {"status": "email_sent", "result": result}

        return {"status": "email_mock"}

    # TELEGRAM 
    if action == "send_telegram":
        text = escape_telegram_text(
            f"🚨 Customer {customer_id} with churn score ({churn_score})"
        )

        if USE_REAL_SERVICES and telegram_enabled():
            result = send_telegram_message(text)
            return {"status": "telegram_sent", "result": result}

        return {"status": "telegram_mock"}

    # MEET + CALENDAR + EMAIL + AUDIT 
    if action == "schedule_meeting_with_meet":

        start = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
        end = (datetime.utcnow() + timedelta(hours=25)).isoformat() + "Z"

        attendees = [os.getenv("GMAIL_RECIPIENT")]

        # Calendar + Meet
        event = create_event_with_meet(
            summary=f"Retention sync: {customer_id}",
            description=f"Churn score: {churn_score}",
            start=start,
            end=end,
            attendees=attendees
        )

        meet_link = (
            event.get("conferenceData", {})
                 .get("entryPoints", [{}])[0]
                 .get("uri")
        )

        # Email + link
        send_email(
            subject=f"[Retention] Meeting {customer_id}",
            body=f"""
Hi,

Customer {customer_id} with churn score  {churn_score}

📅 Event created
🎥 Google Meet:
{meet_link}

Regards,
Auto Retention Agent
"""
        )

        audit_row = [
            datetime.utcnow().isoformat(),
            customer_id,
            churn_score,
            "schedule_meeting_with_meet",
            meet_link
        ]

        # Audit log in Sheets

        append_to_sheet(
            spreadsheet_id=os.getenv("SPREADSHEET_ID"),
            range_name="Sheet1!A:A",
            values=[audit_row]
        )


        return {
            "status": "meet_created",
            "meet_link": meet_link,
            "event_id": event.get("id")
        }

    # DEFAULT
    return {
        "status": "no_action",
        "action_received": action
    }
