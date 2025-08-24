
from celery import shared_task
from .models import Company
from django.db import transaction
from .logger import log

import random



@shared_task
def update_company_price_on_schedule():
    try:        
        companies = Company.objects.all()
        
        with transaction.atomic():
            for company in companies:
                random_price = round(random.uniform(1,1000),2)
                log.info(f"Price is triggerd : {random_price}")
                company.price = random_price
                log.info(f"Price is set to price field of company : {random_price}")
            
            Company.objects.bulk_update(companies,['price'])
            log.info(f"Price updating completed : {random_price}")
        
    except Exception as err:
        print(str(err))