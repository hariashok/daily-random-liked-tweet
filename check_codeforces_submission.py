import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HANDLE = "envariant"

STATE_FILE = "state/last_submission_id.txt"


def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})


def get_latest_submission():
    url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=1"
    return requests.get(url).json()["result"][0]


def read_last_submission_id():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except:
        return ""


def write_last_submission_id(sub_id):
    os.makedirs("state", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(sub_id))


def main():
    submission = get_latest_submission()

    current_id = str(submission["id"])
    last_id = read_last_submission_id()

    # 🔥 KEY LOGIC
    if current_id != last_id:
        problem = submission["problem"]
        problem_name = problem["name"]
        contest_id = problem.get("contestId", "N/A")
        problem_index = problem.get("index", "")

        time_str = submission["creationTimeSeconds"]

        if contest_id != "N/A":
            problem_link = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
            submission_link = f"https://codeforces.com/contest/{contest_id}/submission/{current_id}"
        else:
            problem_link = "N/A"
            submission_link = f"https://codeforces.com/submission/{current_id}"

        message = (
            "🟢 New submission detected!\n\n"
            f"📘 Problem: {problem_index}. {problem_name}\n"
            f"🔗 Problem: {problem_link}\n"
            f"🔗 Submission: {submission_link}"
        )

        send_message(message)

        write_last_submission_id(current_id)

        print("NOTIFIED")

    else:
        print("No new submission.")


if __name__ == "__main__":
    main()
