from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index_view, name='base'),
    path('client/', views.client_view, name='client'),
    path('buster/', views.buster_view, name='buster'),
    path('shop/', views.shop_view, name='shop'),
    path('cart/<account_slug>/', views.shop_cart_view, name='add_to_cart'),
    path('bust/', views.shop_bust, name='bust'),
    url(r'^cart_bust$', views.bust_cart_view, name='add_to_bust'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout')
]

# boost\/\?mmr_from\=[0-9]{1,4}\&mmr_to\=[0-9]{1,4}$
