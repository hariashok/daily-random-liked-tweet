import os
import requests
import random

# Environment variables (you will add these in GitHub Secrets)
TWITTER_USER_ACCESS_TOKEN = os.environ.get("TWITTER_USER_ACCESS_TOKEN")
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Twitter API base
BASE_URL = "https://api.twitter.com/2"

def get_user_id(username):
    url = f"{BASE_URL}/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {TWITTER_USER_ACCESS_TOKEN}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()["data"]["id"]

def get_liked_tweets(user_id):
    url = f"{BASE_URL}/users/{user_id}/liked_tweets?max_results=100&tweet.fields=created_at,author_id,public_metrics,text&expansions=author_id&user.fields=name,username"
    headers = {"Authorization": f"Bearer {TWITTER_USER_ACCESS_TOKEN}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def format_tweet(tweet, includes):
    text = tweet["text"]
    created = tweet["created_at"]
    tweet_id = tweet["id"]
    author_id = tweet["author_id"]

    # Find author details
    author = None
    for u in includes.get("users", []):
        if u["id"] == author_id:
            author = u
            break

    author_name = author["name"] if author else "Unknown"
    author_username = author["username"] if author else ""

    tweet_url = f"https://twitter.com/{author_username}/status/{tweet_id}"

    return f"{author_name} (@{author_username})\n\n{text}\n\n{tweet_url}"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    res = requests.post(url, data=payload)
    res.raise_for_status()

def main():
    user_id = get_user_id(TWITTER_USERNAME)
    data = get_liked_tweets(user_id)

    tweets = data.get("data", [])
    includes = data.get("includes", {})

    if not tweets:
        send_to_telegram("No liked tweets found for your account.")
        return

    random_tweet = random.choice(tweets)
    message = format_tweet(random_tweet, includes)

    send_to_telegram(message)

if __name__ == "__main__":
    main()
