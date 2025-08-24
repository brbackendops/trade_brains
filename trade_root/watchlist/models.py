from django.db import models
from django.conf import settings


# Create your models here.

class WatchList(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False,blank=True)
    company = models.ManyToManyField('company.Company',related_name='companies')
    
    
    class Meta:
        verbose_name = "watchlist"
        verbose_name_plural = "watchlists"
    
    def __str__(self) -> str:
        return self.name