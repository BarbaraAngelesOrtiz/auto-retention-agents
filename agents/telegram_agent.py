import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def telegram_enabled() -> bool:
    """Verifica si Telegram está configurado correctamente"""
    return all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID])

def send_telegram_message(text: str) -> dict:
    """Envía un mensaje por Telegram"""
    if not telegram_enabled():
        return {"ok": False, "error": "Telegram not configured"}

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "MarkdownV2"  # opcional
    }
    response = requests.post(url, json=payload)
    try:
        return response.json()
    except Exception:
        return {"ok": False, "error": "Failed to parse response from Telegram"}
