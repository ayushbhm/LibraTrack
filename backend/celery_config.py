from celery import Celery
from celery.schedules import crontab
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Create a Celery instance
celery = Celery('my_app')

# Update Celery configuration
celery.conf.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2',
    timezone='Asia/Kolkata',  # Set your timezone
    beat_schedule={
        'daily-reminder-task': {
            'task': 'tasks.daily_reminder',  # Ensure this matches the task name in tasks.py
            'schedule': crontab(hour=0, minute=21),  # Runs every day at 9:11 PM
        },
    },
)

# Import tasks explicitly to ensure they are discovere

import tasks
