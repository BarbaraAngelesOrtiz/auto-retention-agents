from dotenv import load_dotenv
load_dotenv()

# test_gmail_token.py
from agents.gmail_agent import get_gmail_service

get_gmail_service()  # This will open the browser and ask for authorization.
print("Token de Gmail generado correctamente.")

# test_calendar_token.py
from agents.google_calendar_agent import get_calendar_service

service = get_calendar_service()  # The browser will open to authorize
print("Token de Google Calendar generado correctamente.")

# test_sheets_token.py
from agents.google_sheets_agent import get_sheets_service

service = get_sheets_service()  # It will open the browser for Sheets
print("Token de Google Sheets generado correctamente.")

