# agents/action_agent.py

import os
from datetime import datetime, timedelta
from collections import Counter
from agents.google_agents import send_email, create_event_with_meet, append_to_sheet
from agents.telegram_agent import send_telegram_message, telegram_enabled
from agents.decision_agent import decide_action
from collections import Counter, defaultdict

CRITICAL_CHURN_ALERT = 100  # If there are more than 100 critical clients → Telegram alert

ACTION_CONTEXT = {
    "run_id": datetime.utcnow().isoformat(),
}

# Main function

def execute_actions(customer_actions):
    """
    Execute all actions:
    1. Derive decisions using decision_agent
    2. Calendar event with Meet for critical clients
    3. Email critical alert
    4. Telegram critical alert
    5. Email general summary
    6. Google Sheets: actions per client + summary
    """
    results = {}

    # Apply decision_agent to each client
  
    for c in customer_actions:
        decision = decide_action(c)
        c.update(decision)  # adds: decision_type, action_suggestion, urgency, value, flags

    # Identify critical customers

    critical_customers = [
    c for c in customer_actions
    if c.get("urgency") == "CRITICAL" or c.get("urgency") == "HIGH"
]
    critical_event = None

    if critical_customers:
        top_customer = max(critical_customers, key=lambda x: x["churn_prob"])
        critical_event = {
            "top_customer_id": top_customer["customer_id"],
            "top_churn_prob": top_customer["churn_prob"],
            "affected_customers": len(critical_customers),
        }

        # Create a Calendar event with Meet
    
        start = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
        end = (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat() + "Z"
        attendees = os.getenv("MEETING_ATTENDEES", "").split(",")

        event = create_event_with_meet(
            summary="🚨 Urgent Retention Meeting",
            description=f"""
Critical churn detected.
Top customer: {critical_event['top_customer_id']}
Churn prob: {critical_event['top_churn_prob']}
Affected customers: {critical_event['affected_customers']}
""",
            start=start,
            end=end,
            attendees=attendees,
        )

        meet_link = event.get("hangoutLink", "No Meet Link")
        critical_event["meet_link"] = meet_link

        # Critical alert email
        
        body_lines = [
            f"A critical churn scenario was detected.\n",
            f"Top customer: {critical_event['top_customer_id']}",
            f"Churn probability: {critical_event['top_churn_prob']}",
            f"Affected customers: {critical_event['affected_customers']}\n",
            "Customer action details:\n"
            f"📅 Google Meet has been scheduled: {meet_link}",
        ]

        send_email(
            subject="🚨 Critical Churn Alert – Meeting Scheduled. Action Details",
            body="\n".join(body_lines)
        )

    # Telegram Alert
    
    if telegram_enabled() and len(critical_customers) >= CRITICAL_CHURN_ALERT:
        send_telegram_message(
            f"🚨 EXTREME CHURN DETECTED\n"
            f"{len(critical_customers)} critical customers.\n"
            f"Meet meeting scheduled for immediate review."
        )
        results["telegram"] = "sent"

    # Email summary
    
    # Initialization of all possible categories
    decision_types = ["REQUIRES_HUMAN_CONTACT", "AUTOMATED_PROMO", "LOYALTY_ENGAGEMENT", "NO_ACTION"]
    manager_summary = Counter({k: 0 for k in decision_types})
    manager_summary.update(c["decision_type"] for c in customer_actions)
    summary_lines = [f"{k}: {v}" for k, v in manager_summary.items()]

    # Count by action_suggestion
    
    possible_actions = [a.get("action_suggestion", "NO_ACTION") for a in customer_actions]
    action_counter = Counter({k: 0 for k in possible_actions})
    action_counter.update(a.get("action_suggestion", "NO_ACTION") for a in customer_actions)
    actions_summary_str = "\n".join([f"- {k}: {v}" for k, v in action_counter.items()])

    # Flag count
    
    all_flags = set(f for a in customer_actions for f in a.get("flags", []))
    flags_counter = Counter({k: 0 for k in all_flags})
    flags_counter.update(f for a in customer_actions for f in a.get("flags", []))
    flags_summary_str = "\n".join([f"- {k}: {v}" for k, v in flags_counter.items()])

    # Count by customer value
    
    possible_values = ["LOW", "MEDIUM", "HIGH", "UNKNOWN"]
    value_counter = Counter({k: 0 for k in possible_values})
    value_counter.update(a.get("value", "UNKNOWN") for a in customer_actions)
    value_summary_str = "\n".join([f"- {k}: {v}" for k, v in value_counter.items()])

    send_email(
        subject="📊 Daily Customer Retention Summary",
        body=f"""Hello Team,

Here is the daily retention summary:

{chr(10).join(summary_lines)}

Critical customers: {len(critical_customers)} 

Actions suggested:
{actions_summary_str}

Flags:
{flags_summary_str}

Customer value:
{value_summary_str}

Best regards,
Retention Bot
"""
    )
    results["summary_email"] = "sent"

    # Save individual actions in Google Sheets

    append_customer_actions(customer_actions)

    # Save global summary in Sheets
    append_summary_to_sheet(manager_summary)

    results["audit"] = "done"
    return results

# Auxiliary functions

def append_customer_actions(actions):
    """Save row by row in Sheets using append_to_sheet original"""
    for a in actions:
        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "customer_id": a.get("customer_id"),
            "decision_type": a.get("decision_type"),
            "churn_prob": a.get("churn_prob"),
            "urgency": a.get("urgency"),
            "action_suggestion": a.get("action_suggestion"),
            "value": a.get("value"),
            "flags": ",".join(a.get("flags", []))  
        }
        append_to_sheet(row)

def append_summary_to_sheet(summary):
    """Save manager_summary in Sheets"""
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "run_id": ACTION_CONTEXT.get("run_id", ""),
        **summary
    }
    append_to_sheet(row)
