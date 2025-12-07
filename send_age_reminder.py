import os
import requests
from datetime import date

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BIRTHDATE = date(1998, 4, 10)  # Your birthday

def calculate_age():
    today = date.today()

    years = today.year - BIRTHDATE.year
    months = today.month - BIRTHDATE.month
    days = today.day - BIRTHDATE.day

    if days < 0:
        months -= 1
        # Adjust days
        prev_month = (today.month - 1) if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        # last day of previous month
        import calendar
        days += calendar.monthrange(prev_year, prev_month)[1]

    if months < 0:
        years -= 1
        months += 12

    return years, months, days

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def main():
    years, months, days = calculate_age()

    msg = (
        f"⏳ Time is precious — you are now {years} years, {months} months, {days} days old today.\n\n"
        "Make today count:\n"
        "• Pick your top-1 task and work on it for 3 hours.\n"
        "• Small, consistent wins compound into big results.\n\n"
        "Reminder sent by your future self — use this moment well."
    )

    send_message(msg)

if __name__ == "__main__":
    main()
