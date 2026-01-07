# services/calendar_service.py

import os

class CalendarService:
    """Interfaz para servicios de calendario."""

    def create_meeting(self, title: str, datetime: str, participants: list):
        raise NotImplementedError("Debe implementar la función en subclase.")


class MockCalendarService(CalendarService):
    """Mock para pruebas locales."""

    def create_meeting(self, title: str, datetime: str, participants: list):
        meeting_id = "MOCK-12345"
        print(f"[MOCK] Meeting scheduled: {title} at {datetime} for {participants}")
        return {"status": "scheduled", "meeting_id": meeting_id, "provider": "mock"}


class MicrosoftCalendarService(CalendarService):
    """Stub para Microsoft Graph API (implementación futura)."""

    def create_meeting(self, title: str, datetime: str, participants: list):
        # Aquí iría la llamada a Microsoft Graph
        meeting_id = "MS-12345"
        print(f"[MICROSOFT] Meeting scheduled: {title} at {datetime} for {participants}")
        return {"status": "scheduled", "meeting_id": meeting_id, "provider": "microsoft"}


def get_calendar_service() -> CalendarService:
    provider = os.getenv("CALENDAR_PROVIDER", "mock").lower()
    if provider == "microsoft":
        return MicrosoftCalendarService()
    else:
        return MockCalendarService()
