from celery import Celery
from django_redis import get_redis_connection

redis_client = get_redis_connection('default')
app = Celery('tasks', broker=redis_client)

@app.task
def add(x,y):
    return x + y


add.delay(4,4)