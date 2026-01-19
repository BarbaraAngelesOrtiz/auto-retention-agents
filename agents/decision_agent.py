# agents/decision_agent.py

from typing import Dict, Any, List
from datetime import datetime

# Decision matrix with business rules

DECISION_MATRIX = [
    # HIGH RISK + HIGH VALUE (CRITICAL)
{"churn_min": 0.7, "value": "HIGH", "flags": ["INACTIVITY_RISK"],
"action": "Urgent call + exclusive benefit + dedicated account manager",
"urgency": "CRITICAL"},

{"churn_min": 0.6, "value": "HIGH", "flags": ["FINANCIAL_RISK"],
"action": "Meeting with manager + personalized value plan + temporary strategic discount",
"urgency": "CRITICAL"},

{"churn_min": 0.6, "value": "HIGH", "flags": ["PROMO_ABUSE"],
"action": "Retention call + migration to premium loyalty program without discounts",
"urgency": "HIGH"},

# HIGH RISK + MEDIUM VALUE
{"churn_min": 0.6, "value": "MEDIUM", "flags": ["INACTIVITY_RISK"],
"action": "Personalized email + reactivation coupon + benefits reminder",
"urgency": "HIGH"},

{"churn_min": 0.6, "value": "MEDIUM", "flags": ["FINANCIAL_RISK"],
"action": "Automated email + financing/installment offer + entry-level products",
"urgency": "HIGH"},

{"churn_min": 0.6, "value": "MEDIUM", "flags": ["PROMO_ABUSE"],
"action": "Email with points program + non-monetary benefits",
"urgency": "MEDIUM"},

# HIGH RISK + LOW VALUE

{"churn_min": 0.6, "value": "LOW", "flags": ["INACTIVITY_RISK"],
"action": "Automated reactivation email + moderate discount",
"urgency": "MEDIUM"},

{"churn_min": 0.5, "value": "LOW", "flags": ["FINANCIAL_RISK"],
"action": "Email with affordable products + referral program",
"urgency": "MEDIUM"},

{"churn_min": 0.6, "value": "LOW", "flags": ["PROMO_ABUSE"],
"action": "Email with product education + limited-time discount",
"urgency": "MEDIUM"},

# LOW RISK + HIGH VALUE (PROACTIVE LOYALTY)

{"churn_min": 0.0, "churn_max": 0.3, "value": "HIGH", "flags": [],
"action": "Automatic VIP program + early access + exclusive events",
"urgency": "LOW"},

{"churn_min": 0.3, "churn_max": 0.5, "value": "HIGH", "flags": [],
"action": "Proactive check-in + surprise benefit + feedback request",
"urgency": "LOW"},
]

# Derive value and flags from the client

def derive_customer_flags(customer: Dict[str, Any]):
    flags = []

    avg_purchase = float(customer.get("avg_purchase_value", 0))

    if avg_purchase > 300: 
        value = "HIGH"
    elif avg_purchase > 100:
        value = "MEDIUM"
    else:
        value = "LOW"

    # Risk flags
    if int(customer.get("days_since_last_purchase", 0)) > 90:
        flags.append("INACTIVITY_RISK")

    if int(customer.get("income_bracket_Low", 0)) == 1:
        flags.append("FINANCIAL_RISK")

    if int(customer.get("promo_flag", 0)) == 1 or float(customer.get("avg_discount_used", 0)) > 0.4:
        flags.append("PROMO_ABUSE")

    return value, flags

# Main decision function

def decide_action(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    churn_prob = float(customer_data.get("churn_prob", 0))
    value, flags = derive_customer_flags(customer_data)
    customer_data["value"] = value
    customer_data["flags"] = flags

    action_suggestion = "Standard review"
    urgency = "LOW"

    for rule in DECISION_MATRIX:
        churn_min = rule.get("churn_min", 0)
        churn_max = rule.get("churn_max", 1.0)
        if not (churn_min <= churn_prob <= churn_max):
            continue

        if rule["value"] != "ANY" and rule["value"] != value:
            continue

        if all(f in flags for f in rule.get("flags", [])):
            action_suggestion = rule["action"]
            urgency = rule["urgency"]
            break

    if urgency == "CRITICAL":
        decision_type = "REQUIRES_HUMAN_CONTACT"
    elif urgency == "HIGH":
        decision_type = "AUTOMATED_PROMO"
    elif urgency == "MEDIUM":
        decision_type = "LOYALTY_ENGAGEMENT"
    else:
        decision_type = "NO_ACTION"

    return {
        "customer_id": customer_data.get("customer_id"),
        "churn_prob": round(churn_prob, 3),
        "decision_type": decision_type,
        "action_suggestion": action_suggestion,
        "urgency": urgency,
        "value": value,
        "flags": flags
    }

def batch_decisions(customers: List[Dict[str, Any]]):
    actions = []
    summary = {"REQUIRES_HUMAN_CONTACT": 0, "AUTOMATED_PROMO": 0,
               "LOYALTY_ENGAGEMENT": 0, "NO_ACTION": 0}

    for c in customers:
        decision = decide_action(c)
        actions.append(decision)
        summary[decision["decision_type"]] += 1

    # Detect if there is a critical event
    critical_event = next(
        (d for d in actions if d["urgency"] == "CRITICAL"), None
    )

    return {
        "customer_actions": actions,
        "manager_summary": summary,
        "critical_event": critical_event
    }
