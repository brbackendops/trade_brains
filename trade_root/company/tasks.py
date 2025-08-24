
from celery import shared_task
from .models import Company
from django.db import transaction
import random


@shared_task
def update_company_price_on_schedule():
    try:        
        companies = Company.objects.all()
        
        with transaction.atomic():
            for company in companies:
                random_price = round(random.uniform(1,1000),2)
                company.price = random_price
            
            Company.objects.bulk_update(companies,['price'])
        
    except Exception as err:
        print(str(err))