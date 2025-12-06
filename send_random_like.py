import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def main():
    # Read all tweet links
    with open("tweets.txt", "r") as f:
        links = [line.strip() for line in f.readlines() if line.strip()]

    if not links:
        msg = "No tweet links saved."
    else:
        msg = random.choice(links)

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    )

if __name__ == "__main__":
    main()
