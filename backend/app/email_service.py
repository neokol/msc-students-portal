import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email: str, lesson_title: str, grade: float):
    smtp_server = 'localhost'
    smtp_port = 1025
    body = f"Your grade in the {lesson_title} lesson has been confirmed and finalized at {grade}"

    msg = MIMEMultipart()
    msg['From'] = 'Grade System'
    msg['To'] = email
    msg['Subject'] = f"Grade on {lesson_title} confirmed"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.send_message(msg)
        print("Email sent to recipient")
    except Exception as e:
        print(f"Failed to send email: {e}")
