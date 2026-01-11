from dotenv import load_dotenv
load_dotenv()

from agents.action_agent import execute_action

print("=== TEST CALENDAR + MEET ===")

result = execute_action(
    action="schedule_meeting_with_meet",
    customer_id="C123",
    churn_score=0.82
)

print("Result:", result)
