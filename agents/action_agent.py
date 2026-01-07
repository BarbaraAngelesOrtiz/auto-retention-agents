# agents/action_agent.py

from services.calendar_service import get_calendar_service

calendar_service = get_calendar_service()

def execute_action(action: str, customer_name: str):
    """
    Ejecuta la acción decidida por el DecisionAgent.
    """
    if action == "schedule_meeting":
        meeting = calendar_service.create_meeting(
            title=f"Retention meeting: {customer_name}",
            datetime="2026-01-06T10:00",  # fecha fija para MVP
            participants=[customer_name, "account_manager@example.com"]
        )
        return meeting
    elif action == "send_message":
        print(f"[ACTION] Sending retention message to {customer_name}")
        return {"status": "message_sent", "customer": customer_name}
    else:
        print(f"[ACTION] No action required for {customer_name}")
        return {"status": "no_action", "customer": customer_name}
