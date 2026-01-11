# agents/gmail_agent.py
import os
import json
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE")
GMAIL_RECIPIENT = os.getenv("GMAIL_RECIPIENT")

def get_gmail_service():
    creds = None
    # Si existe token guardado, lo usamos
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Si no hay token válido, generamos uno
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        # Guardamos el token para futuros usos
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    
    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(subject: str, body: str, recipient: str = None):
    if not recipient:
        recipient = GMAIL_RECIPIENT
    if not recipient:
        return {"ok": False, "error": "No recipient configured"}

    service = get_gmail_service()
    message = {
        "raw": base64.urlsafe_b64encode(
            f"To: {recipient}\r\nSubject: {subject}\r\n\r\n{body}".encode()
        ).decode()
    }
    try:
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        return {"ok": True, "id": sent_message.get("id")}
    except Exception as e:
        return {"ok": False, "error": str(e)}
