from dotenv import load_dotenv
load_dotenv()

# test_gmail_token.py
from agents.gmail_agent import get_gmail_service

get_gmail_service()  # Esto abrirá el navegador y pedirá autorización
print("Token de Gmail generado correctamente.")

# test_calendar_token.py
from agents.google_calendar_agent import get_calendar_service

service = get_calendar_service()  # abrirá el navegador para autorizar
print("Token de Google Calendar generado correctamente.")

# test_sheets_token.py
from agents.google_sheets_agent import get_sheets_service

service = get_sheets_service()  # abrirá el navegador para Sheets
print("Token de Google Sheets generado correctamente.")

