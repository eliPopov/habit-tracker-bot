from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
from datetime import datetime

app = Flask(__name__)

HABITS = ["HelpWithJob", "FunMoment", "PlanADate", "Exercise"]

def log_response(date, responses):
    conn = sqlite3.connect("habit_data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS habits 
                 (date TEXT, habit TEXT, status TEXT)''')
    for habit, status in zip(HABITS, responses):
        c.execute("INSERT INTO habits (date, habit, status) VALUES (?, ?, ?)",
                  (date, habit, status))
    conn.commit()
    conn.close()

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip().lower()
    date = datetime.now().strftime("%Y-%m-%d")
    responses = incoming_msg.split()

    if len(responses) != len(HABITS):
        reply = "❌ Invalid format. Please reply like: yes no yes"
    else:
        log_response(date, responses)
        reply = "✅ Got it! Logged today's check-in."

    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5050)