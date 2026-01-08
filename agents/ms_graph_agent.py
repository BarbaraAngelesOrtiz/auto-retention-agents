# agents/ms_graph_agent.py
import requests
from msal import ConfidentialClientApplication
import os

# Credenciales de Azure AD (variables de entorno)
CLIENT_ID = os.getenv("MS_CLIENT_ID")
CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
TENANT_ID = os.getenv("MS_TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

def schedule_meeting(subject: str, start: str, end: str, attendees: list) -> dict:
    """
    Crea una reunión en Microsoft Outlook Calendar usando Graph API
    """
    if not CLIENT_ID or not CLIENT_SECRET or not TENANT_ID:
        return {"status": "Microsoft credentials not set"}

    try:
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )
        token_response = app.acquire_token_for_client(scopes=SCOPE)
        access_token = token_response.get("access_token")
        if not access_token:
            return {"status": "Could not acquire token", "details": token_response}

        url = "https://graph.microsoft.com/v1.0/me/events"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        data = {
            "subject": subject,
            "start": {"dateTime": start, "timeZone": "UTC"},
            "end": {"dateTime": end, "timeZone": "UTC"},
            "attendees": [{"emailAddress": {"address": a, "name": a}, "type": "required"} for a in attendees]
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    except Exception as e:
        return {"status": "error", "error": str(e)}
