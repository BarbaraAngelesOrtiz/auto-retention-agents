from agents.gmail_agent import send_email

result = send_email(
    to="tu_correo@gmail.com",
    subject="Test de agentes 🚀",
    body="Hola! Esto es una prueba desde mi proyecto de churn."
)
print(result)
