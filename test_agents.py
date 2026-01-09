# test_agents.py
import os
from datetime import datetime, timedelta, timezone
from agents.ms_graph_agent import ms_graph_healthcheck, create_calendar_event, ms_graph_enabled
from agents.telegram_agent import send_telegram_message

print("=== TEST MS GRAPH HEALTHCHECK ===")
if not ms_graph_enabled():
    print("⚠️ Microsoft Graph no está configurado. Ignorando healthcheck.")
else:
    result = ms_graph_healthcheck()
    print("Graph Healthcheck Result:", result)

print("\n=== TEST MS GRAPH CALENDAR ===")
if not ms_graph_enabled():
    print("⚠️ Microsoft Graph no configurado. Saltando creación de evento.")
else:
    start = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
    end = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
    subject = "Test Event from AutoRetention"
    body = "Este evento fue creado automáticamente para probar MS Graph"

    calendar_result = create_calendar_event(
        subject=subject,
        body=body,
        start=start,
        end=end
    )
    print("Calendar Event Result:", calendar_result)

print("\n=== TEST TELEGRAM MESSAGE ===")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("⚠️ Telegram no configurado. Saltando envío de mensaje.")
else:
    text = "🚨 Este es un mensaje de prueba desde AutoRetention Agents"
    telegram_result = send_telegram_message(text)
    print("Telegram Result:", telegram_result)
