import os
import requests
from datetime import datetime, timezone, timedelta

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HANDLE = "envariant"

IST = timezone(timedelta(hours=5, minutes=30))

STATE_FILE = "state/last_notified.txt"


def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})


def get_submissions():
    url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=50"
    return requests.get(url).json()["result"]


def read_last_notified():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except:
        return ""


def write_last_notified(date_str):
    os.makedirs("state", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(date_str)


def main():
    now_ist = datetime.now(IST)
    today_str = str(now_ist.date())

    # 🔥 KEY FIX: last 24 hours window
    cutoff_time = now_ist - timedelta(hours=24)

    submissions = get_submissions()
    last_notified = read_last_notified()

    found_recent = None

    for sub in submissions:
        ts = sub["creationTimeSeconds"]
        sub_dt = datetime.fromtimestamp(ts, IST)

        if sub_dt >= cutoff_time:
            found_recent = sub
            break

    if found_recent and last_notified != today_str:
        problem = found_recent["problem"]
        problem_name = problem["name"]
        contest_id = problem.get("contestId", "N/A")
        problem_index = problem.get("index", "")
        submission_id = found_recent["id"]

        sub_dt = datetime.fromtimestamp(found_recent["creationTimeSeconds"], IST)
        time_str = sub_dt.strftime("%I:%M %p")

        if contest_id != "N/A":
            problem_link = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
            submission_link = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"
        else:
            problem_link = "N/A"
            submission_link = f"https://codeforces.com/submission/{submission_id}"

        message = (
            "🟢 Green detected (recent submission)!\n\n"
            f"⏰ Time: {time_str} IST\n"
            f"📘 Problem: {problem_index}. {problem_name}\n"
            f"🔗 Problem: {problem_link}\n"
            f"🔗 Submission: {submission_link}"
        )

        send_message(message)

        # save today's notification state
        write_last_notified(today_str)

        print("NOTIFIED")

    else:
        print("No recent submission or already notified.")


if __name__ == "__main__":
    main()
