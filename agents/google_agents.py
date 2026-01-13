# agents/google_agents.py

import os
from dotenv import load_dotenv
load_dotenv() 

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# LOAD CREDENTIALS
GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")
GMAIL_RECIPIENT = os.getenv("GMAIL_RECIPIENT")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/presentations"
]

def get_credentials():
    creds = Credentials(
        None,
        refresh_token=GMAIL_REFRESH_TOKEN,
        client_id=GMAIL_CLIENT_ID,
        client_secret=GMAIL_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES
    )
    creds.refresh(Request())
    return creds

# GMAIL
def send_gmail_message(to: str, subject: str, body: str):
    """Send an email using the Gmail API"""
    try:
        import base64
        from email.mime.text import MIMEText

        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_result = service.users().messages().send(
            userId="me",
            body={"raw": encoded_message}
        ).execute()

        return {"status": "ok", "message_id": send_result['id']}
    except HttpError as e:
        return {"status": "error", "error": str(e)}

# CALENDAR
def create_calendar_event(title: str, description: str, start: str, end: str, attendees=None):
    """Create an event in Google Calendar"""
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': title,
            'description': description,
            'start': {'dateTime': start, 'timeZone': 'UTC'},
            'end': {'dateTime': end, 'timeZone': 'UTC'},
        }
        if attendees:
            event['attendees'] = [{'email': a} for a in attendees]

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return {"status": "ok", "event_id": created_event['id']}
    except HttpError as e:
        return {"status": "error", "error": str(e)}

# SPREADSHEET 
def append_to_spreadsheet(row_data: dict):
    """Add a row to Google Sheets"""
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        values = [list(row_data.values())]
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1",
            valueInputOption="RAW",
            body=body
        ).execute()
        return {"status": "ok", "updates": result.get('updates', {})}
    except HttpError as e:
        return {"status": "error", "error": str(e)}

# GOOGLE DOCS 
def create_doc(title: str, content: str):
    """Create a document in Google Docs"""
    try:
        creds = get_credentials()
        service = build('docs', 'v1', credentials=creds)
        doc = service.documents().create(body={"title": title}).execute()
        doc_id = doc['documentId']
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}
        ).execute()
        return {"status": "ok", "doc_id": doc_id}
    except HttpError as e:
        return {"status": "error", "error": str(e)}

# GOOGLE SLIDES 
def create_slide(title: str, content: str):
    """Create a presentation in Google Slides"""
    try:
        creds = get_credentials()
        service = build('slides', 'v1', credentials=creds)
        presentation = service.presentations().create(body={"title": title}).execute()
        pres_id = presentation['presentationId']
        
        # Add first slide with title and content
        service.presentations().batchUpdate(
            presentationId=pres_id,
            body={"requests": [
                {"createSlide": {"slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"}}},
                {"insertText": {"objectId": presentation['slides'][0]['objectId'], "text": content}}
            ]}
        ).execute()
        return {"status": "ok", "presentation_id": pres_id}
    except HttpError as e:
        return {"status": "error", "error": str(e)}
