from django.urls import path, include
from . import views

app_name = 'providus'

urlpatterns = [
    path('', views.ProvidusDashboard, name='providus_home'),
    path('balance/', views.AccountBalance, name='balance'),
    path('status/', views.TransactionStatus, name='status'),
    path('search/', views.SearchTransaction, name='search'),
    path('mail/', views.MailUser, name='mail')

]
