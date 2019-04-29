from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index_view, name='index'),
    path('client', views.client_view, name='client'),
    path('booster', views.booster_view, name='booster'),
]
