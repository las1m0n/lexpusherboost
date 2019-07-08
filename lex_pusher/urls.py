from django.conf.urls import url
from django.urls import path
from .views import PayView, PayCallbackView

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('client/', views.client_view, name='client'),
    path('buster/', views.buster_view, name='buster'),

    path('bust/', views.bust_shop_view, name='bust'),
    path('shop/', views.accs_shop_view, name='shop'),

    path('to_busters/', views.buster_login_view, name='to_busters'),
    path('new_buster/', views.buster_register_view, name='new_booster'),

    path('cart/<account_slug>/', views.accs_shop_cart_view, name='cart_account'),
    path('cart_bust/', views.bust_shop_cart_view, name='cart_bust'),

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),

    path('buster/new_stat/', views.new_stat_view, name='new_stat'),
    path('buster/change_info/', views.buster_info_change_view, name='change_info_account'),
    path('buster/info/<bust_id>/', views.bust_info_view, name='bust_info'),
    path('buster/info/take/<bust_id>/', views.take_bust_view, name='bust_take'),

    url(r'^pay/$', PayView.as_view(), name='buster_payout'),
    url(r'^pay-callback/$', PayCallbackView.as_view(), name='pay_callback'),
]
