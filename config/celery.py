import os
from celery import Celery
from django.conf import settings
from django_redis import get_redis_connection
from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('trades_app', broker=f'redis://{config('REDIS_CLIENT')}/1')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def check():
    print("I am checking your stuff")


app.conf.beat_schedule = {
    "interval_10s": {
        "task": "tasks.check",
        "schedule": 30.0
    }
}