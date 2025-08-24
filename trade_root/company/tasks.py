
from celery import shared_task
from .models import Company
import random


@shared_task
def update_company_price_on_schedule(price):
    try:
        price = round(random.uniform(1,1000),2)
        Company.objects.update()
    except Exception as err:
        pass