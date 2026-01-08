# utils/churn_simulator.py
import random
import pandas as pd

def simulate_churn(customer: dict) -> float:
    import random
    import pandas as pd

    score = 0.5

    # Loyalty
    loyalty = customer.get("loyalty_program", "No")
    if str(loyalty).lower() == "yes":
        score -= 0.15

    # Membership years
    membership_years = customer.get("membership_years")
    try:
        membership_years = float(membership_years)
        score -= min(membership_years * 0.02, 0.1)
    except (TypeError, ValueError):
        pass

    # Days since last purchase
    days = customer.get("days_since_last_purchase", 30)
    try:
        days = float(days)
        score += min(days / 100, 0.3)
    except (TypeError, ValueError):
        pass

    # Total sales
    total_sales = customer.get("total_sales", 0)
    try:
        total_sales = float(total_sales)
        if total_sales < 500:
            score += 0.1
    except (TypeError, ValueError):
        pass

    # Purchase frequency
    freq = customer.get("purchase_frequency")
    try:
        freq = float(freq)
        if freq < 5:
            score += 0.05
    except (TypeError, ValueError):
        pass

    # Promotion effectiveness
    promo_eff = customer.get("promotion_effectiveness")
    try:
        promo_eff = float(promo_eff)
        score -= promo_eff * 0.15
    except (TypeError, ValueError):
        pass

    # Aleatoriedad
    score += random.uniform(-0.05, 0.05)

    # Limitar entre 0 y 1
    score = max(0, min(1, score))
    return round(score, 2)

