from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Account, Bust, Stat
from .forms import ShopCartForm, BoostCartForm, ClientForm
from django.urls import reverse


def index_view(request):
    return render(request, 'lex_pusher/index.html', {})


def client_view(request):
    # if

    client_id = 1

    bust = Bust.objects.get(client_id=client_id)
    stats = Stat.objects.filter(bust_id=bust.id)

    context = {
        'stats_times': [str(i.time) for i in stats],
        'stats_values': [i.mmr for i in stats],
    }

    print(context)

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
        new_boost = form.save(commit=False)
        new_client = form_acc.save(commit=False)
        email = form_acc.cleaned_data['email']
        vk = form_acc.cleaned_data['vk']
        skype = form_acc.cleaned_data['skype']
        phone = form_acc.cleaned_data['phone']
        steam_login = form.cleaned_data['steam_login']
        steam_password = form.cleaned_data['steam_password']
        new_boost.mmr_from = mmr_from
        new_boost.mmr_to = mmr_to
        new_boost.steam_login = steam_login
        new_boost.steam_password = steam_password
        new_client.email = email
        new_client.skype = skype
        new_client.phone = phone
        new_client.vk = vk
        new_client.password = "12345678"
        new_boost.save()
        new_client.save()
        return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form,
        'form_acc': form_acc,
        'mmr_from': mmr_from,
        'mmr_to': mmr_to,
    }
    return render(request, 'lex_pusher/client/bust_form.html', context)


