import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def main():
    # Read all tweet links from file
    with open("tweets.txt", "r") as f:
        links = [line.strip() for line in f.readlines() if line.strip()]

    if not links:
        message = "No tweet links found in tweets.txt"
    else:
        message = random.choice(links)

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message}
    )

if __name__ == "__main__":
    main()
