import os
import requests
from datetime import datetime, timezone, timedelta

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Allowed trigger times (HH:MM in IST)
TRIGGER_TIMES = {
    "06:00",
    "11:00",
    "14:30",
    "19:00",
    "21:00",
}

def main():
    now_ist = datetime.now(IST).strftime("%H:%M")

    if now_ist not in TRIGGER_TIMES:
        print(f"Not trigger time ({now_ist} IST). Exiting.")
        return

    message = (
        "🧠 17 second rule manifestation\n\n"
        "https://x.com/AlpacaAurelius/status/2014079615938015236?s=20"
    )

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message}
    )

    print(f"Message sent at {now_ist} IST")

if __name__ == "__main__":
    main()
