# agents/decision_agent.py

def decide_action(churn_score: float, customer_value: float) -> str:
    """
    Decide la acción a tomar según churn_score y valor del cliente.
    
    Returns:
        'no_action', 'send_message', 'schedule_meeting'
    """
    if churn_score >= 0.8 and customer_value >= 1000:
        return "schedule_meeting"
    elif churn_score >= 0.6:
        return "send_message"
    else:
        return "no_action"
