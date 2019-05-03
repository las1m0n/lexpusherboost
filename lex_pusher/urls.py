from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index_view, name='base'),
    path('client/', views.client_view, name='client'),
    path('booster/', views.booster_view, name='booster'),
    path('shop/', views.shop_view, name='shop'),
    path('cart/<account_slug>/', views.shop_cart_view, name='add_to_cart'),
    path('boost/', views.shop_boost, name='boost'),
    path('boost/?mmr_from=<int:mmr_from>&mmr_to=<int:mmr_to>/', views.boost_cart_view, name='add_to_boost'),
]
