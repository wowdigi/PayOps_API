from django.urls import path, include
from . import views

app_name = 'agent'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('requery/', views.RequeryView, name='requery'),
    path('retry/', views.RetryView, name='retry'),
    path('balance/', views.BalanceView, name='balance'),
    path('refresh/', views.RefreshView, name='refresh'),
]
