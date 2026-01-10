# agents/google_calendar_agent.py
import os
from dotenv import load_dotenv

load_dotenv() 

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")

def get_calendar_service():
    print(f"DEBUG: Usando archivo de credenciales: {CREDS_FILE}")
    flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
    # Puerto fijo para evitar redirect_uri_mismatch
    creds = flow.run_local_server(port=8080)
    print("DEBUG: Token obtenido correctamente")
    service = build("calendar", "v3", credentials=creds)
    return service

def create_event(summary, description, start, end, attendees=[]):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start, "timeZone": "UTC"},
        "end": {"dateTime": end, "timeZone": "UTC"},
        "attendees": [{"email": a} for a in attendees],
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"DEBUG: Evento creado: {created_event.get('htmlLink')}")
    return created_event

