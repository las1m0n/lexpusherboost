from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('client/', views.client_view, name='client'),
    path('buster/', views.buster_view, name='buster'),

    path('bust/', views.shop_bust, name='bust'),
    path('shop/', views.shop_view, name='shop'),

    path('to_busters/', views.buster_login_view, name='to_busters'),
    path('new_buster/', views.buster_register_view, name='new_booster'),

    path('cart/<account_slug>/', views.shop_cart_view, name='cart_account'),
    path('cart_bust/', views.bust_cart_view, name='cart_bust'),

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),



    path('test/', views.test, name='test')
    path('logout/', views.logout_view, name='logout'),
    path('buster_cabinet/change_info/', views.buster_info_change_view, name='change_info_account'),
    path('buster_cabinet/info/<bust_id>/', views.bust_info_view, name='bust_info'),
    path('buster_cabinet/info/take/<bust_id>/', views.take_bust_view, name='bust_take')
]
