from worker import celery_init_app
from app import create_app

app = create_app()
celery = celery_init_app(app)
