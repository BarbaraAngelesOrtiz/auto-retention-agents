# test_agents.py
from dotenv import load_dotenv
load_dotenv()

from agents.ms_graph_agent import ms_graph_healthcheck, create_calendar_event, ms_graph_enabled
from agents.telegram_agent import send_telegram_message
from datetime import datetime, timedelta, timezone

print("=== TEST MS GRAPH HEALTHCHECK ===")
if ms_graph_enabled():
    health_result = ms_graph_healthcheck()
    print("Graph Healthcheck Result:", health_result)
else:
    print("⚠️ Microsoft Graph no está configurado. Ignorando healthcheck.")

print("\n=== TEST MS GRAPH CALENDAR ===")
if ms_graph_enabled():
    # Fechas en UTC
    start = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
    end = (datetime.now(timezone.utc) + timedelta(hours=1, minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")
    
    try:
        calendar_result = create_calendar_event(
            subject="Evento de prueba desde agentes 🚀",
            body="Esto es un test automático de creación de eventos",
            start=start,
            end=end
        )
        print("Calendar Event Result:", calendar_result)
    except Exception as e:
        print("Error creando evento:", e)
else:
    print("⚠️ Microsoft Graph no configurado. Saltando creación de evento.")

print("\n=== TEST TELEGRAM MESSAGE ===")
try:
    telegram_result = send_telegram_message("Mensaje de prueba desde agentes 🚀")
    print("Telegram Result:", telegram_result)
except Exception as e:
    print("⚠️ Telegram no configurado o error:", e)
