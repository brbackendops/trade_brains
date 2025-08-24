import os
from celery import Celery
from django.conf import settings
from decouple import config
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('trades_app')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def check():
    pass


app.conf.CELERY_RESULT_BACKEND = f'redis://127.0.0.1:6379/0'
app.conf.beat_schedule = {
    "schedule_tasks": {
        "task": "trade_root.company.tasks.update_company_price_on_schedule",
        "schedule": crontab(minute='*/1')
    }
}


