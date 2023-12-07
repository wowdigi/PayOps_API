from django.db import models
from django.db.models.aggregates import Max

# Create your models here.
class ServiceTypeModel(models.Model):
    network = models.CharField(max_length=12)
    
    def __str__(self) -> str:
        return self.network
    
class DataBundleModel(models.Model):
    pass
