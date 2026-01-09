# test_agents.py

from datetime import datetime, timedelta, timezone
from agents.ms_graph_agent import create_calendar_event, ms_graph_healthcheck, ms_graph_enabled
from agents.telegram_agent import send_telegram_message

print("=== TEST MS GRAPH HEALTHCHECK ===")
if ms_graph_enabled():
    health = ms_graph_healthcheck()
    print("Healthcheck Graph:", health)
else:
    print("⚠️ Microsoft Graph no está configurado. Ignorando healthcheck.")

print("\n=== TEST MS GRAPH CALENDAR ===")
# Configuramos fechas
start_dt = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
end_dt = (datetime.now(timezone.utc) + timedelta(hours=1, minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")

if ms_graph_enabled():
    res = create_calendar_event(
        subject="Test Event",
        body="Evento de prueba desde test_agents.py",
        start_dt=start_dt,
        end_dt=end_dt
    )
    print("Calendar Event Result:", res)
else:
    print("⚠️ Microsoft Graph no configurado. Saltando creación de evento.")

print("\n=== TEST TELEGRAM MESSAGE ===")
text = "Mensaje de prueba desde test_agents.py "
res_telegram = send_telegram_message(text)
print("Telegram Result:", res_telegram)
