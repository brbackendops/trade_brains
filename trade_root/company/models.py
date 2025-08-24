from django.db import models
from datetime import datetime

# Create your models here.

class Company(models.Model):
    companyy_name = models.CharField(max_length=255,blank=False,null=False)
    price = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        indexes = [
            models.Index(fields=['companyy_name'], name='company_name_idx')
        ]
    
    def __str__(self) -> str:
        return self.companyy_name

class CompanyInfo(models.Model):
    company_id = models.OneToOneField(Company,on_delete=models.CASCADE,blank=False,null=False,related_name="company_info")
    symbol = models.CharField(max_length=255,blank=False,null=False)
    scrip_code = models.CharField(max_length=255,blank=False,null=False)
    created_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "company_info"
        verbose_name_plural = "company_infos"
    
    
    def __str__(self) -> str:
        return self.company_id.companyy_name + f"({self.symbol})"
