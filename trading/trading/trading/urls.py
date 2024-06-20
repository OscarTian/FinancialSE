"""
URL configuration for trading project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app import views as app_views
from stock import views as stock_views
urlpatterns = [
    path('show_stock_info/<int:pk>/', stock_views.show_stock_info),
    path('get_stock_data/<int:pk>/', stock_views.get_stock_data),
    path('register/', app_views.register),
    path('', admin.site.urls),
]
