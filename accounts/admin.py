# from django.contrib import admin
# from .models import *

# # Register your models here.
# admin.site.register(ProfileModel)
# admin.site.register(OrganisationAPIKey)

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import CreateUserForm, ProfileModelForm
from .models import OrganisationAPIKey, Transaction, Organisation
from rest_framework_api_key.admin import APIKeyModelAdmin

# Register your models here.
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = ProfileModelForm
    model = CustomUser
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'organisation'
    ]

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info', {
                'fields': ('organisation',)
            }
        ),
    )


@admin.register(OrganisationAPIKey)
class OrganisationAPIKeyModelAdmin(APIKeyModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = (
        'beneficiary_AccountName', 'transaction_Amount', 'transaction_Status',
        'narration', 'beneficiary_Bank', 'customer', 'transaction_Ref', 'transaction_Date',
    )

    list_filter = ('transaction_Date', )


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Organisation)
# admin.site.register(ProfileModel)
# admin.site.register(ProfileModel)

admin.site.site_header = 'geekops Portal'
