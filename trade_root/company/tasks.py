
from celery import shared_task
import random


@shared_task
def update_company_price_on_schedule(price):
    try:
        pass
    except Exception as err:
        pass