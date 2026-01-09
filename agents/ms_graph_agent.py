# agents/ms_graph_agent.py
import os
import requests

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_TENANT_ID = os.getenv("MS_TENANT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_USER_EMAIL = os.getenv("MS_USER_EMAIL")

GRAPH_SCOPE = "https://graph.microsoft.com/.default"


def ms_graph_enabled() -> bool:
    return all([
        MS_CLIENT_ID,
        MS_TENANT_ID,
        MS_CLIENT_SECRET,
        MS_USER_EMAIL
    ])


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

    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

# agents/ms_graph_agent.py
def ms_graph_healthcheck():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    user_email = os.getenv("MS_USER_EMAIL")
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}"
    r = requests.get(url, headers=headers)
    return {
        "status_code": r.status_code,
        "response": r.json()
    }
def create_calendar_event(subject: str, body: str, start_dt: str, end_dt: str):
    """
    Crea un evento simple en el calendario del usuario (Outlook / Graph)
    start_dt / end_dt en formato ISO 8601: 2026-01-08T15:00:00
    """
    token = get_access_token()
    if not token:
        return {"error": "Microsoft Graph not configured"}

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
            "dateTime": start_dt,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_dt,
            "timeZone": "UTC"
        }
    }

    response = requests.post(
        "https://graph.microsoft.com/v1.0/users/{}/events".format(MS_USER_EMAIL),
        headers=headers,
        json=event_payload
    )

    return {
        "status_code": response.status_code,
        "response": response.json()
    }

