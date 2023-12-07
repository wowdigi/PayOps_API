from django.urls import path
from . import views


urlpatterns = [
    path('pay/', views.PayHomeView, name="pay"),
    path('success/', views.SuccessPageView.as_view(), name="success"),
    path('failure/', views.ErrorPageView.as_view(), name="failure"),
    path('buy_airtime/', views.AirtimeView, name="airtime"),
    path('buy_data/', views.DataBundlesView, name="data_bundles"),
    path('pay_dstv/', views.payDSTVView, name="pay_dstv"),
    path('pay_gotv/', views.payGoTVView, name="pay_gotv"),
    path('pay_startimes/', views.payStarTimesView, name="pay_startimes"),
    path('buy_electricity/', views.ElectricityView, name="buy_electricity"),
    path('create_pin/', views.CreatePINView, name="create_pin"),
    path('transfer/', views.BankTransferView, name='transfer'),

]
