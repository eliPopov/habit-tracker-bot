from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
import os

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
YOUR_NUMBER = os.environ.get("YOUR_NUMBER")
import time

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_daily_checklist():
    message = (
        "📋 Daily Check-in:\nDid you complete these?\n"
        "1. Helped her with her job hunt?\n2. Did something fun with her?\n3. Planned/Suggested a date?\n 4. Exercised?"
        "Reply like: yes no yes yes"
    )
    client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to=YOUR_NUMBER
    )

send_daily_checklist() 