# agents/ms_graph_agent.py
import os
import test_api
from datetime import datetime

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_TENANT_ID = os.getenv("MS_TENANT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
GRAPH_SCOPE = "https://graph.microsoft.com/.default"

TEAM_ID = os.getenv("TEAM_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def ms_graph_enabled() -> bool:
    return all([MS_CLIENT_ID, MS_TENANT_ID, MS_CLIENT_SECRET])

def get_access_token():
    if not ms_graph_enabled():
        return None

    token_url = f"https://login.microsoftonline.com/{MS_TENANT_ID}/oauth2/v2.0/token"

    payload = {
        "client_id": MS_CLIENT_ID,
        "client_secret": MS_CLIENT_SECRET,
        "scope": GRAPH_SCOPE,
        "grant_type": "client_credentials"
    }

    response = test_api.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def ms_graph_healthcheck():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    user_email = os.getenv("MS_USER_EMAIL")  # debe ser el UPN completo
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}"
    r = test_api.get(url, headers=headers)
    return {
        "status_code": r.status_code,
        "response": r.json() if r.content else "<empty response>"
    }


def create_calendar_event(subject: str, body: str, start: str, end: str):
    """
    Crea un evento simple en el calendario del usuario (Outlook / Graph)
    start / end en formato ISO 8601: 2026-01-08T15:00:00
    """

    token = get_access_token()
    if not token:
        return {"error": "Microsoft Graph not configured"}

    MS_USER_EMAIL = os.getenv("MS_USER_EMAIL")  # <- Asegurarse de definirlo aquí
    if not MS_USER_EMAIL:
        return {"error": "MS_USER_EMAIL no definido"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    event_payload = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": body
        },
        "start": {
            "dateTime": start,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end,
            "timeZone": "UTC"
        }
    }

    url = f"https://graph.microsoft.com/v1.0/users/{MS_USER_EMAIL}/events"

    response = test_api.post(url, headers=headers, json=event_payload)

    try:
        response_json = response.json()
    except Exception:
        response_json = "<empty response>"

    return {"status_code": response.status_code, "response": response_json}

def send_email(subject, body):
    token = get_access_token()
    url = f"https://graph.microsoft.com/v1.0/users/{MS_FROM_EMAIL}/sendMail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body},
            "toRecipients": [{"emailAddress": {"address": MS_TO_EMAIL}}]
        }
    }
    r = test_api.post(url, headers=headers, json=payload)
    return {"status_code": r.status_code, "response": r.text}

def send_teams_message(message):
    token = get_access_token()
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"body": {"content": message}}
    r = test_api.post(url, headers=headers, json=payload)
    return {"status_code": r.status_code, "response": r.text}
