from dotenv import load_dotenv
load_dotenv()

from agents.google_calendar_agent import create_event

event = create_event(
    summary="Prueba Retención Cliente",
    description="Evento generado por agente",
    start="2026-01-11T10:00:00Z",
    end="2026-01-11T11:00:00Z",
    attendees=["barbaraortiz1501@gmail.com"]  # reemplaza con tu email
)

print(event)
