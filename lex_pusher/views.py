from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Account
from .forms import ShopCartForm, BoostCartForm
from django.urls import reverse


def index_view(request):
    return render(request, 'lex_pusher/index.html', {})


def client_view(request):
    # if


    return render(request, 'lex_pusher/client/lk_client.html', {})


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
    mmr_from = request.GET.get("mmr_from", "")
    mmr_to = request.GET.get("mmr_to", "")
    if form.is_valid():
        new_boost = form.save(commit=False)
        email = form.cleaned_data['email']
        login = form.cleaned_data['login']
        password = form.cleaned_data['password']
        vk = form.cleaned_data['vk']
        skype = form.cleaned_data['skype']
        phone = form.cleaned_data['phone']
        new_boost.mmr_from = mmr_from
        new_boost.mmr_to = mmr_to
        new_boost.email = email
        new_boost.login = login
        new_boost.password = password
        new_boost.skype = skype
        new_boost.phone = phone
        new_boost.vk = vk
        new_boost.save()
        return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form,
        'mmr_from': mmr_from,
        'mmr_to': mmr_to,
    }
    return render(request, 'lex_pusher/client/bust_form.html', context)


