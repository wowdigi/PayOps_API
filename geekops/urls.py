"""geekops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('agent/', include('agent.urls')),
    path('', include('bills.urls')),
    path('providus/', include('providusboard.urls')),
]


handler404 = 'bills.views.error_404'
handler500 = 'bills.views.error_500'
# handler403 = 'geekops.views.error_403'
# handler400 = 'geekops.views.error_400'