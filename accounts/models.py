from django.contrib.auth.models import User
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Organisation(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    organisation_name = models.CharField(max_length=100)
    organisation_url = models.URLField()

    def __str__(self):
        return self.organisation_name


class CustomUser(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=20, unique=True, blank=True, null=True)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, null=True, blank=True)
    transaction_Pin = models.IntegerField(default=1234)
    customer_PhoneNumber = models.CharField(
        max_length=15, unique=True, null=True, blank=True)

    user_url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username


class OrganisationAPIKey(AbstractAPIKey):
    organisation_key = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='apikey', null=True, blank=True)

    def __str__(self):
        return str(self.organisation_key)


class Transaction(models.Model):
    beneficiary_AccountName = models.CharField(max_length=100)
    transaction_Amount = models.IntegerField()
    transaction_Status = models.BooleanField(default=False)
    narration = models.TextField()
    beneficiary_Bank = models.CharField(max_length=50)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_Ref = models.CharField(max_length=50, unique=True)
    transaction_Date = models.DateTimeField(auto_now_add=True)
    transaction_Type = models.CharField(max_length=30)
