from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
from twilio_config import *
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

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_checklist, 'cron', hour=9, minute=0)  # 9:00 AM
scheduler.start()

# Keep alive
while True:
    time.sleep(60)