import smtplib
import pandas as pd
import datetime
import time
import schedule
import os
import requests
import base64
from dotenv import load_dotenv
from email.message import EmailMessage

# Load environment variables
load_dotenv()
SMTP_SERVER = "smtp.mailersend.net"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Read CSV file
df = pd.read_csv("birthdays.csv")

# Read email template
def get_email_body(name):
    with open("email_template.html", "r", encoding="utf-8") as file:
        return file.read().replace("{{name}}", name)

# Convert image to base64
def download_image(url):
    response = requests.get(url)
    return response.content if response.status_code == 200 else None

# Send Email
def send_email(recipient_email, name, photo_url):
    msg = EmailMessage()
    msg["Subject"] = f"🎂 A Special Birthday Surprise for You, {name}!"
    msg["From"] = SMTP_USERNAME
    msg["To"] = [recipient_email, "samarthseh@gmail.com"]

    email_body = get_email_body(name)
    msg.set_content("Your email client does not support HTML emails.")
    msg.add_alternative(email_body, subtype="html")

    # Attach Image
    image_data = download_image(photo_url)
    if image_data:
        msg.add_attachment(image_data, maintype="image", subtype="jpeg", filename="birthday.jpg", cid="image1")

    # Send Email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
    print(f"Email sent to {recipient_email} and samarthseh@gmail.com")

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
