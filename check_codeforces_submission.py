import os
import requests
from datetime import datetime, timezone, timedelta

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HANDLE = "envariant"

# IST timezone
IST = timezone(timedelta(hours=5, minutes=30))


def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})


def get_latest_submission():
    url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=1"
    res = requests.get(url).json()
    return res["result"][0]


def main():
    now_ist = datetime.now(IST).date()

    submission = get_latest_submission()

    timestamp = submission["creationTimeSeconds"]
    submission_dt = datetime.fromtimestamp(timestamp, IST)
    submission_date = submission_dt.date()

    # Problem details
    problem = submission["problem"]
    problem_name = problem["name"]
    contest_id = problem.get("contestId", "N/A")
    problem_index = problem.get("index", "")

    # Submission ID
    submission_id = submission["id"]

    # Links
    if contest_id != "N/A":
        problem_link = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
        submission_link = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"
    else:
        problem_link = "N/A"
        submission_link = f"https://codeforces.com/submission/{submission_id}"

    # File to track last notification
    file_path = "last_notified.txt"

    try:
        with open(file_path, "r") as f:
            last_notified = f.read().strip()
    except:
        last_notified = ""

    # Send message only once per day
    if str(submission_date) == str(now_ist) and last_notified != str(now_ist):

        time_str = submission_dt.strftime("%I:%M %p")

        message = (
            "🔥 He did today's test!\n\n"
            f"⏰ Time: {time_str} IST\n"
            f"📘 Problem: {problem_index}. {problem_name}\n"
            f"🔗 Problem: {problem_link}\n"
            f"🔗 Submission: {submission_link}"
        )

        send_message(message)

        with open(file_path, "w") as f:
            f.write(str(now_ist))


if __name__ == "__main__":
    main()
