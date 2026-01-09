# test_agents.py

from dotenv import load_dotenv
load_dotenv()
from agents.ms_graph_agent import ms_graph_healthcheck, create_calendar_event, ms_graph_enabled
from agents.telegram_agent import send_telegram_message, telegram_enabled
from datetime import datetime, timedelta, timezone

print("=== TEST MS GRAPH HEALTHCHECK ===")
if ms_graph_enabled():
    health_result = ms_graph_healthcheck()
    print("Graph Healthcheck Result:", health_result)
else:
    print("⚠️ Microsoft Graph no está configurado. Ignorando healthcheck.")

print("\n=== TEST MS GRAPH CALENDAR ===")
if ms_graph_enabled():
    start = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
    end = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
    calendar_result = create_calendar_event(
        subject="Test Event",
        body="Evento de prueba generado automáticamente",
        start=start,
        end=end
    )
    print("Calendar Event Result:", calendar_result)
else:
    print("⚠️ Microsoft Graph no configurado. Saltando creación de evento.")

print("\n=== TEST TELEGRAM MESSAGE ===")
if telegram_enabled():
    telegram_result = send_telegram_message("Mensaje de prueba desde agentes 🚀")
    print("Telegram Result:", telegram_result)
else:
    print("⚠️ Telegram no configurado. Saltando envío de mensaje.")
