def simulate_churn_score(tenure, monthly_charges, support_tickets):
    score = 0.0

    if tenure < 6:
        score += 0.3
    if monthly_charges > 80:
        score += 0.3
    if support_tickets > 3:
        score += 0.3

    return min(score, 0.99)
