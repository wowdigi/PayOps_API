from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.editProfile, name="profile"),
    path('api_request/', views.apiRequest, name="api_request"),
    path('initial/', views.CustomUserAPIView.as_view(), name='initial')
]
