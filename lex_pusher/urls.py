from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    # test
    path('singleacc', views.single_acc_test, name='single_acc_test'),
    path('404', views.fourOfour, name='fourOfour'),
    # start/index
    path('', views.index_view, name='index'),
    # client
    path('client/', views.client_view, name='client'),
    # buster
    path('buster/', views.buster_view, name='buster'),
    path('to_busters/', views.buster_login_view, name='to_busters'),
    path('new_buster/', views.buster_register_view, name='new_booster'),
    path('buster/new_stat/', views.new_stat_view, name='new_stat'),
    path('buster/change_info/', views.buster_info_change_view, name='change_info_account'),
    path('buster/info/<bust_id>/', views.bust_info_view, name='bust_info'),
    path('buster/info/take/<bust_id>/', views.take_bust_view, name='bust_take'),
    # calibration
    path('calibration/', views.calibration_view, name='calibration'),
    path('calibration/cart/', views.calibration_cart_view, name='calibration_cart'),
    path('calibration/cart/pay/', views.calibration_cart_end_view, name='cal_end'),
    # bust
    path('bust/', views.bust_shop_view, name='bust'),
    path('bust/cart/confirm/', views.bust_confirm_view, name='bust_confirm'),
    path('cart_bust/', views.bust_shop_cart_view, name='cart_bust'),
    # shop
    path('shop/', views.accs_shop_view, name='shop'),
    path('shop/account/<account_id>/', views.accs_id_view, name='account_info'),
    path('cart/<account_slug>/', views.accs_shop_cart_view, name='cart_account'),
    path('shop/cart/confirm/', views.acc_shop_end_view, name='shop_account_end'),
    url(r'^success/$', views.pay_success, name="success"),
    path('success_payout/<id>/', views.payout_view, name="payout"),
    path('buster_logout/', views.buster_logout, name="logout_buster"),
    # log(in/out)
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
]
