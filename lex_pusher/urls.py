from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index_view, name='base'),
    path('client/', views.client_view, name='client'),
    path('booster/', views.booster_view, name='booster'),
    path('shop/', views.shop_view, name='shop'),
    path('cart/<account_slug>/', views.shop_cart_view, name='add_to_cart'),
    path('boost/', views.shop_boost, name='boost')
]
