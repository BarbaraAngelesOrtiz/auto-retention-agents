# agents/google_sheets_agent.py
import os
import numpy as np
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
TOKEN_FILE = os.getenv("SHEETS_TOKEN_FILE")

def get_sheets_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    service = build("sheets", "v4", credentials=creds)
    return service

def write_to_sheet(spreadsheet_id: str, range_name: str, values: list[list]):
    """Sobrescribe valores en un rango específico"""
    service = get_sheets_service()
    body = {"values": values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    return result

def append_to_sheet(spreadsheet_id: str, range_name: str, values: list[list]):
    """Agrega valores al final de la hoja"""
    service = get_sheets_service()
    body = {"values": values}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    return result

