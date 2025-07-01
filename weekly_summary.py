import sqlite3
from datetime import datetime, timedelta
from twilio.rest import Client
import os

# Get Twilio credentials from GitHub Actions environment
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
YOUR_NUMBER = os.environ.get("YOUR_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

HABITS = ["Meditate", "Exercise", "Read"]

def get_weekly_summary():
    conn = sqlite3.connect("habit_data.db")
    c = conn.cursor()
    
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    week_start = week_ago.strftime("%Y-%m-%d")
    week_end = today.strftime("%Y-%m-%d")

    summary = {}

    for habit in HABITS:
        c.execute("""
            SELECT COUNT(*) FROM habits 
            WHERE habit = ? AND status = 'yes' AND date BETWEEN ? AND ?
        """, (habit, week_start, week_end))
        count = c.fetchone()[0]
        summary[habit] = count

    conn.close()
    return summary

def send_summary():
    summary = get_weekly_summary()
    message = "📊 Weekly Summary:\n"
    for habit, count in summary.items():
        emoji = "🧘" if habit == "Meditate" else "🏃" if habit == "Exercise" else "📚"
        message += f"{emoji} {habit}: ✅ {count}/7\n"

    client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to=YOUR_NUMBER
    )

send_summary()