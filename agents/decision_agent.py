# agents/decision_agent.py
import random

def decide_action(churn_score: float, mode: str = "deterministic") -> str:
    """
Decide the action to take based on the churn score.
:param churn_score: value between 0 and 1
:param mode: "deterministic" (default) or "random"
:return: name of the action
    """
    if mode == "deterministic":
        if churn_score >= 0.85:
            return "schedule_meeting_with_meet"
        elif churn_score >= 0.6:
            return "send_email"
        elif churn_score >= 0.4:
            return "send_telegram"  
        else:
            return "no_action"
    
    elif mode == "random":
        # Probabilities according to churn_score
        if churn_score >= 0.85:
            return random.choices(
                ["schedule_meeting_with_meet", "send_email", "send_telegram", "no_action"],
                weights=[0.6, 0.2, 0.15, 0.05],
                k=1
            )[0]
        elif churn_score >= 0.6:
            return random.choices(
                ["send_email", "send_telegram", "schedule_meeting_with_meet", "no_action"],
                weights=[0.5, 0.3, 0.1, 0.1],
                k=1
            )[0]
        elif churn_score >= 0.4:
            return random.choices(
                ["send_telegram", "send_email", "no_action", "schedule_meeting_with_meet"],
                weights=[0.5, 0.2, 0.25, 0.05],
                k=1
            )[0]
        else:
            return random.choices(
                ["no_action", "send_telegram", "send_email", "schedule_meeting_with_meet"],
                weights=[0.7, 0.2, 0.08, 0.02],
                k=1
            )[0]

    else:
        raise ValueError(f"Unknown mode: {mode}")
