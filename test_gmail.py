from agents.gmail_agent import send_email

result = send_email(
    recipient="barbaraortiz1501@gmail.com",  # ✅ usar 'recipient'
    subject="Test de agentes 🚀",
    body="Hola! Esto es una prueba desde mi proyecto de churn."
)
print(result)
