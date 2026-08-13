import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
load_dotenv()


SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_reset_link(user_email : str,reset_link : str) : 
    msg = MIMEText(f"click here to reset your password {reset_link}")
    msg["subject"] = "Password reset link"
    msg["From"] = SMTP_USER
    msg["To"] = user_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure connection
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
