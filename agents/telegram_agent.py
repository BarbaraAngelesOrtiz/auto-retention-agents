# agents/telegram_agent.py
import requests
import os

# Variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")       # Token de tu bot
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")   # Chat ID de destino

def send_telegram_message(text: str) -> dict:
    """
    Envía un mensaje de Telegram al chat configurado.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "Telegram credentials not set", "text": text}

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "error": str(e)}
