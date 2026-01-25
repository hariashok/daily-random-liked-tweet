import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def main():
    msg = (
        "🧠 17 second rule manifestation\n\n"
        "https://x.com/AlpacaAurelius/status/2014079615938015236?s=20"
    )
    send_message(msg)

if __name__ == "__main__":
    main()
