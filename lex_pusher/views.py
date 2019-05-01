from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse


def index_view(request):
    return render(request, 'lex_pusher/index.html', {})


def client_view(request):
    return render(request, 'lex_pusher/lk_client.html', {})


def booster_view(request):
    return render(request, 'lex_pusher/lk_booster.html', {})


def shop_view(request):
    return render(request, 'lex_pusher/flex_shop.html', {})


