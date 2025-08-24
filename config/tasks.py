from celery import Celery
from django.conf import settings
from django_redis import get_redis_connection
from decouple import config

redis_client = get_redis_connection('default')
app = Celery('tasks', broker=f'redis://{config('REDIS_CLIENT')}/1')

@app.task
def check():
    print("I am checking your stuff")


app.conf.beat_schedule = {
    "interval_10s": {
        "task": "tasks.check",
        "schedule": 30.0
    }
}