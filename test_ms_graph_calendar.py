from dotenv import load_dotenv
load_dotenv()

from agents.ms_graph_agent import create_calendar_event
from datetime import datetime, timedelta, timezone

# Crear fechas ISO 8601 UTC
start = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
end = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")

subject = "Evento de prueba desde Python"
body = "Este evento se creó automáticamente con Microsoft Graph API."

try:
    result = create_calendar_event(subject=subject, body=body, start=start, end=end)
    print("Calendar Event Result:", result)
except Exception as e:
    print("Error creando evento:", e)
