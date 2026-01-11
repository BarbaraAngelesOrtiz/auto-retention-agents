# agents/google_calendar_agent.py
import os
from dotenv import load_dotenv
load_dotenv()

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
TOKEN_FILE = os.getenv("CALENDAR_TOKEN_FILE")

def get_calendar_service():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import pickle
    import os

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
    TOKEN_FILE = os.getenv("CALENDAR_TOKEN_FILE")

    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            try:
                creds = pickle.load(token)
            except EOFError:
                creds = None  # si el token está vacío, se regenerará

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service

def create_event_with_meet(summary, description, start, end, attendees):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start, "timeZone": "UTC"},
        "end": {"dateTime": end, "timeZone": "UTC"},
        "attendees": [{"email": a} for a in attendees if a],
        "conferenceData": {
            "createRequest": {
                "requestId": "meet-" + summary.replace(" ", "-")
            }
        }
    }

    return service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1
    ).execute()
