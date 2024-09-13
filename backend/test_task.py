from backend.celery_config import celery

# Send a test task to the Celery worker
result = celery.send_task('tasks.add', args=[10, 20])
print('Task result:', result.get(timeout=10))


    
celery.send_task('task.daily_reminder', args=["asdf@ggg", "sdfgdf"])