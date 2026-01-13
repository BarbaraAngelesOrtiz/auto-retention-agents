from agents.gmail_agent import send_email

result = send_email(
    recipient= "GMAIL_RECIPIENT",  
    subject="Agent test🚀",
    body="Hi! This is a test from my churn project."
)
print(result)
