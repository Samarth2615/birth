import yagmail
import pandas as pd
import datetime
import time
import schedule
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")  # Your Gmail
APP_PASSWORD = os.getenv("APP_PASSWORD")  # App password

# Read CSV file
df = pd.read_csv("birthdays.csv")

# Read email template
def get_email_body(name, photo_url):
    with open("email_template.html", "r", encoding="utf-8") as file:
        template = file.read()
    return template.replace("{{name}}", name).replace("{{photo}}", photo_url)

# Send Email
def send_email(recipient_email, name, photo_url):
    yag = yagmail.SMTP(EMAIL, APP_PASSWORD)
    subject = f"🎂 Happy Birthday, {name}! 🎉"
    body = get_email_body(name, photo_url)
    yag.send(to=[recipient_email, EMAIL], subject=subject, contents=body)
    print(f"Email sent to {recipient_email} and {EMAIL}")

# Check for birthdays and send emails
def check_and_send():
    today = datetime.datetime.now().strftime("%d/%m")
    for _, row in df.iterrows():
        if row["DOB"] == today:
            send_email(row["email"], row["name"], row["photo"])

# Send test emails after deployment
def send_test_emails():
    for _, row in df.iterrows():
        send_email(row["email"], row["name"], row["photo"])

# Schedule the job
schedule.every().day.at("18:30").do(check_and_send)  # 18:30 UTC = 12:00 AM IST

# Send test email after starting
send_test_emails()

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
