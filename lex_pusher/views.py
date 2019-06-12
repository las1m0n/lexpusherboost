import secrets
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Account, Bust, Stat, Buster
from .forms import ShopCartForm, BustCartForm, ClientForm, LoginForm, BusterApplicationForm, LoginBusterForm
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from datetime import datetime


def index_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password']
        login_user = authenticate(request, username=password, password=password)
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
    form = LoginBusterForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        login_user = authenticate(request, username=username, password=password)
        if login_user is not None:
            login(request, login_user)
            return HttpResponseRedirect(reverse('buster_cabinet'))
        else:
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form
    }
    return render(request, 'lex_pusher/buster/lk_buster.html', context)


def buster_form_view(request):
    form = BusterApplicationForm(request.POST or None)
    if form.is_valid():
        new_buster_application = form.save(commit=False)
        new_buster_application.booster_acc = None
        new_buster_application.save()
        return HttpResponseRedirect(reverse('end_buster'))

    context = {
        'form': form,
    }
    return render(request, 'lex_pusher/buster/buster_form.html', context)


def buster_client_view(request):
    buster = Buster.objects.filter(booster_acc=request.user).first()
    busts = Bust.objects.filter(buster_id=buster)
    inactive_busts = Bust.objects.filter(is_active=False)
    context = {
        'inactive_busts': inactive_busts,
        'busts': busts,
        'buster': buster
    }
    return render(request, 'lex_pusher/buster/choose_client.html', context)


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


def success_form_view(request):
    return render(request, 'lex_pusher/buster/end_buster.html')


def shop_bust(request):
    return render(request, 'lex_pusher/client/flex_bust.html')


def bust_cart_view(request):
    form_bust = BustCartForm(request.POST or None)
    form_acc = ClientForm(request.POST or None)
    mmr_from = request.GET.get("mmr_from", "")
    mmr_to = request.GET.get("mmr_to", "")
    if form_bust.is_valid() and form_acc.is_valid():
        email = form_acc.cleaned_data['email']
        vk = form_acc.cleaned_data['vk']
        skype = form_acc.cleaned_data['skype']
        phone = form_acc.cleaned_data['phone']
        steam_login = form_bust.cleaned_data['steam_login']
        steam_password = form_bust.cleaned_data['steam_password']
        secret_key = secrets.token_hex(nbytes=8)
        CustomUser.objects.create_user(
            email=email,
            skype=skype,
            phone=phone,
            vk=vk,
            username=secret_key,
            password=secret_key,
        )

        login_user = authenticate(username=secret_key, password=secret_key)
        if login_user:
            login(request, login_user)

        Bust.objects.create(
            client=request.user,
            mmr_from=mmr_from,
            mmr_to=mmr_to,
            steam_login=steam_login,
            steam_password=steam_password
        )
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
