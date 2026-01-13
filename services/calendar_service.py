# services/calendar_service.py

import os

class CalendarService:
    """Interface for calendar services."""

    def create_meeting(self, title: str, datetime: str, participants: list):
        raise NotImplementedError("You must implement the function in a subclass.")


class MockCalendarService(CalendarService):
    """Mock for local testing."""

    def create_meeting(self, title: str, datetime: str, participants: list):
        meeting_id = "MOCK-12345"
        print(f"[MOCK] Meeting scheduled: {title} at {datetime} for {participants}")
        return {"status": "scheduled", "meeting_id": meeting_id, "provider": "mock"}


class MicrosoftCalendarService(CalendarService):
    """Stub for Microsoft Graph API (future implementation)."""

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
