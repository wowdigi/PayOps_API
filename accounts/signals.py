from accounts.admin import CustomUser
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import OrganisationAPIKey
from django.dispatch import receiver
from django.contrib.auth import get_user_model
#from rest_framework_api_key.models import APIKey
CustomUser = get_user_model()


@receiver(post_save, sender=CustomUser)
def create_apikey(sender, instance, created, **kwargs):
    if created:
        c, key = OrganisationAPIKey.objects.create_key(name=instance.username)
        user = get_user_model().objects.get(username=instance.username)
        user.key = key
        c.organisation_key = instance
        c.save()
        user.save()
    else:
        instance.apikey.save()