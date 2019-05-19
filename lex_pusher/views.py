import secrets
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Account, Bust, Stat, Buster
from .forms import ShopCartForm, BoostCartForm, ClientForm, LoginForm
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from users.models import CustomUser
from modules import opendota
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


def update_stat(bust):
    ratings = opendota.ratings(bust.steam_id)
    stats = Stat.objects.filter(bust_id=bust.id)
    stats = [stat.match_id for stat in stats]

    for r in ratings:
        if r['match_id'] in stats:
            continue
        if not r['solo_competitive_rank']:
            continue
        if r['time'].date() < bust.start_date:
            continue

        stat = Stat(
            bust_id=bust,
            match_id=r['match_id'],
            mmr=r['solo_competitive_rank'],
            time=r['time']
        )
        stat.save()


def client_view(request):
    bust = Bust.objects.filter(client=request.user)
    print(bust.all()[1])
    stats = Stat.objects.filter(bust_id=bust.all()[1])

    update_stat(bust)

    context = {
        'stats_times': [i.time.strftime("%m.%d, %H:%M") for i in stats],
        'stats_values': [i.mmr for i in stats],
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
        email = form.cleaned_data['email']
        skype = form.cleaned_data['skype']
        phone = form.cleaned_data['phone']
        new_purchase_account.solo_mmr = account.solo_mmr
        new_purchase_account.party_mmr = account.party_mmr
        new_purchase_account.account_slug = account.slug
        new_purchase_account.email = email
        new_purchase_account.skype = skype
        new_purchase_account.phone = phone
        new_purchase_account.save()
        return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'lex_pusher/accs/shop_cart.html', context)


def shop_bust(request):
    context = {}
    return render(request, 'lex_pusher/client/flex_bust.html', context)


def bust_cart_view(request):
    form = BoostCartForm(request.POST or None)
    form_acc = ClientForm(request.POST or None)
    mmr_from = request.GET.get("mmr_from", "")
    mmr_to = request.GET.get("mmr_to", "")
    if form.is_valid():
        form.save(commit=False)
        form_acc.save(commit=False)
        email = form_acc.cleaned_data['email']
        vk = form_acc.cleaned_data['vk']
        skype = form_acc.cleaned_data['skype']
        phone = form_acc.cleaned_data['phone']
        steam_login = form.cleaned_data['steam_login']
        steam_password = form.cleaned_data['steam_password']
        secret = secrets.token_hex(nbytes=8)
        Bust.objects.create(
            client=None,
            mmr_from=mmr_from,
            mmr_to=mmr_to,
            steam_id=1111,
            steam_login=steam_login,
            steam_password=steam_password
        )
        CustomUser.objects.create_user(
            email="data@"+secret,
            skype=skype,
            phone=phone,
            vk=vk,
            username=email,
            password=secret,
        )
        return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form,
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
