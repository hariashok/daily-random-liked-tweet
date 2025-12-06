import os
import requests
import random
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")

NITTER_BASE = "https://nitter.net"

def fetch_likes(username):
    url = f"{NITTER_BASE}/{username}/likes"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    tweets = []
    for tweet in soup.select(".timeline-item"):
        content = tweet.select_one(".tweet-content")
        author = tweet.select_one(".fullname")
        handle = tweet.select_one(".username")
        link = tweet.select_one("a.tweet-link")

        if content and author and handle and link:
            tweets.append({
                "text": content.get_text(strip=True),
                "author": author.get_text(strip=True),
                "handle": handle.get_text(strip=True),
                "url": NITTER_BASE + link["href"]
            })

    return tweets

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def main():
    tweets = fetch_likes(TWITTER_USERNAME)

    if not tweets:
        send_to_telegram("No liked tweets found (via Nitter).")
        return

    tweet = random.choice(tweets)

    msg = f"{tweet['author']} {tweet['handle']}\n\n{tweet['text']}\n\n{tweet['url']}"
    send_to_telegram(msg)

if __name__ == "__main__":
    main()
