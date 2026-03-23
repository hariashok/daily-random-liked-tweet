import os
import requests
from datetime import datetime, timezone, timedelta

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HANDLE = "envariant"

IST = timezone(timedelta(hours=5, minutes=30))


def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})


def main():
    now_ist = datetime.now(IST)
    today = now_ist.date()

    url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=20"
    res = requests.get(url).json()
    submissions = res["result"]

    file_path = "last_notified.txt"

    print("Script started")

url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=5"
res = requests.get(url).json()
print(res)
    try:
        with open(file_path, "r") as f:
            last_notified = f.read().strip()
    except:
        last_notified = ""

    found = None

    for sub in submissions:
        ts = sub["creationTimeSeconds"]
        sub_dt = datetime.fromtimestamp(ts, IST)

        if sub_dt.date() == today and sub.get("verdict") == "OK":
            found = sub
            break

    if found and last_notified != str(today):
        problem = found["problem"]
        problem_name = problem["name"]
        contest_id = problem.get("contestId", "N/A")
        problem_index = problem.get("index", "")
        submission_id = found["id"]

        time_str = sub_dt.strftime("%I:%M %p")

        problem_link = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
        submission_link = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"

        message = (
            "🟢 Nathan completed today's problem!\n\n"
            f"⏰ Time: {time_str} IST\n"
            f"📘 Problem: {problem_index}. {problem_name}\n"
            f"🔗 Problem: {problem_link}\n"
            f"🔗 Submission: {submission_link}"
        )

        send_message(message)

        with open(file_path, "w") as f:
            f.write(str(today))


if __name__ == "__main__":
    main()
