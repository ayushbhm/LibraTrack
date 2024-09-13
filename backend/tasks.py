import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from celery_config import celery
from datetime import datetime, timedelta
from celery import Celery, shared_task
from celery.schedules import crontab
from controllers.mailservice import send_message

from model_checking import fetch_inactive_user_emails

@celery.task
def add(x, y):
    return x + y

@celery.task
def daily_reminder(subject="daily reminder"):
    today = datetime.now().date()
    user_emails = user_emails = fetch_inactive_user_emails()
    subject = "ghj"
    for email in user_emails:
        send_message(to=email, subject=subject, content_body="<html>Daily reminder content</html>")

    return "Daily reminder sent"




