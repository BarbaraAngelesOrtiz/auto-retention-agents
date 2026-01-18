# tests/agents/test_google_agents.py
from datetime import datetime, timedelta
from agents.google_agents import send_email, create_event_with_meet, append_to_sheet
import os

def test_gmail():
    print(" TEST GMAIL ")
    subject = "Test Email from Auto Retention Agent"
    body = f"This is a test email sent at {datetime.utcnow().isoformat()} UTC"
    result = send_email(subject, body, recipient=os.getenv("GMAIL_RECIPIENT"))
    print(result)

def test_calendar_meet():
    print("\n TEST CALENDAR + MEET ")
    start = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(hours=25)).isoformat() + "Z"
    summary = "Test Retention Meeting"
    description = "This is a test meeting with Meet link."
    attendees = [os.getenv("GMAIL_RECIPIENT")]  
    result = create_event_with_meet(summary, description, start, end, attendees)
    print(result)

def test_sheets():
    print("\n TEST GOOGLE SHEETS")
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "customer_id": "TEST_CUST_001",
        "churn_score": 0.5,
        "action": "test_action",
        "notes": "Test append to sheet"
    }
    result = append_to_sheet(row)
    print(result)

if __name__ == "__main__":
    test_gmail()
    test_calendar_meet()
    test_sheets()
