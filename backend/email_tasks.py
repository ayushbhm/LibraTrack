# backend/tasks/email_tasks.py
from flask_mail import Message
from app import app, mail, celery

@celery.task
def send_daily_email(recipient):
    with app.app_context():
        msg = Message("Daily Email",
                      sender="your-email@example.com",
                      recipients=[recipient])
        msg.body = "This is a test email sent from Celery."
        mail.send(msg)
        print(f"Sent daily email to {recipient}")
