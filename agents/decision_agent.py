# agents/decision_agent.py

def decide_action(churn_score: float) -> str:
    """
    Decide qué acción tomar según churn_score
    """
    if churn_score > 0.7:
        return "schedule_meeting"
    elif churn_score > 0.4:
        return "send_email"
    else:
        return "no_action"

