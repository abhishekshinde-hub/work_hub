import smtplib
from email.mime.text import MIMEText
def send_reset_link(user_email : str,reset_link : str) : 
    msg = MIMEText(f"click here to reset your password {reset_link}")
    msg["subject"] = "Password reset link"
    msg["From"] = "workhub@gmail.com"
    msg["To"] = user_email