from dotenv import load_dotenv
load_dotenv()

from agents.telegram_agent import send_telegram_message
from agents.action_agent import escape_telegram_text

text = "Hello! This is a test from the agent."
text = escape_telegram_text(text)

result = send_telegram_message(text)
print(result)
