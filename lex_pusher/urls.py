from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='base'),
    path('client/', views.client_view, name='client'),
    path('buster/', views.buster_view, name='buster'),
    path('buster_cabinet/', views.buster_client_view, name='buster_cabinet'),
    path('new_buster/', views.buster_form_view, name='new_booster'),
    path('success_form/', views.success_form_view, name='end_buster'),
    path('shop/', views.shop_view, name='shop'),
    path('cart/<account_slug>/', views.shop_cart_view, name='add_to_cart'),
    path('buster_cabinet/new_stat/', views.new_stat_view, name='new_stat'),
    path('bust/', views.shop_bust, name='bust'),
    url(r'^cart_bust$', views.bust_cart_view, name='add_to_bust'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('buster_cabinet/change_info/', views.buster_info_change_view, name='change_info_account'),
    path('buster_cabinet/info/<bust_id>/', views.bust_info_view, name='bust_info'),
    path('buster_cabinet/info/take/<bust_id>/', views.take_bust_view, name='bust_take')
]
