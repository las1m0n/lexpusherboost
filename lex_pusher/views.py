import secrets
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Account, Bust, Stat, Buster
from .forms import ShopCartForm, BustCartForm, ClientForm, LoginForm
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from users.models import CustomUser
from datetime import datetime


def index_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password']
        login_user = authenticate(request, email="data@"+password, password=password)
        if login_user is not None:
            login(request, login_user)
            return HttpResponseRedirect(reverse('client'))
        else:
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form
    }
    return render(request, 'lex_pusher/index.html', context)


def client_view(request):
    bust = Bust.objects.filter(client=request.user).first()
    stats = Stat.objects.filter(bust_id=bust.id)

    context = {
        'stats_times': [i.time.strftime("%m.%d, %H:%M") for i in stats],
        'stats_values': [i.mmr for i in stats],
        'bust': bust
    }

    return render(request, 'lex_pusher/client/lk_client.html', context)


def buster_view(request):
    return render(request, 'lex_pusher/buster/lk_buster.html', {})


def shop_view(request):
    accounts = Account.objects.filter(available=True)
    context = {
        'accounts': accounts,
    }
    return render(request, 'lex_pusher/accs/flex_shop.html', context)


def shop_cart_view(request, account_slug):
    account = Account.objects.get(slug=account_slug)
    form = ShopCartForm(request.POST or None)
    if form.is_valid():
        new_purchase_account = form.save(commit=False)
        new_purchase_account.account_slug = account.slug
        new_purchase_account.save()
        return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'lex_pusher/accs/shop_cart.html', context)


def shop_bust(request):
    return render(request, 'lex_pusher/client/flex_bust.html')


def bust_cart_view(request):
    form_bust = BustCartForm(request.POST)
    form_acc = ClientForm(request.POST)

    mmr_from = request.POST.get("mmr_from", 0)
    mmr_to = request.POST.get("mmr_to", 0)
    if form_bust.is_valid() and form_acc.is_valid():
        bust = form_bust.save(commit=False)
        acc = form_acc.save(commit=False)

        bust.mmr_from = mmr_from
        bust.mmr_to = mmr_to
        bust.client = request.user
        acc.password = secrets.token_hex(nbytes=8)
        bust.save()
        acc.save()
        return HttpResponseRedirect(reverse('client'))

    context = {
        'form': form_bust,
        'form_acc': form_acc,
        'mmr_from': mmr_from,
        'mmr_to': mmr_to,
    }
    return render(request, 'lex_pusher/client/bust_form.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('base'))
