# agents/google_sheets_agent.py
import os
import numpy as np
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")  # tu credentials.json
TOKEN_FILE = os.getenv("SHEETS_TOKEN_FILE", "sheets_token.json")

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

def write_to_sheet(range_name, values):
    """
    Escribe valores en Google Sheets
    range_name: Ej: "Sheet1!A1"
    values: lista de listas (filas)
    """
    # Limpiar NaN o None
    clean_values = []
    for row in values:
        clean_row = ["" if (v is None or (isinstance(v, float) and np.isnan(v))) else v for v in row]
        clean_values.append(clean_row)

    service = get_sheets_service()
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,      # Ej: "Sheet1!A1"
            valueInputOption="RAW",
            body={"values": clean_values},
        )
        .execute()
    )
    return result

