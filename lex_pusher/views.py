# -*- coding: utf-8 -*-
# coding: utf-8
from __future__ import unicode_literals
from . import utils
import json
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.edit import CreateView, SingleObjectMixin
from .forms import ShopCartForm, BustCartForm, ClientForm, LoginForm, BusterApplicationForm, LoginBusterForm, \
    UploadFileForm
from .models import Account, Bust, Stat, Buster, Punish
from django.contrib.auth import get_user_model
from meta.views import Meta, MetadataMixin
from mailer import Mailer, Message
from .mail_send import send, send_payout, send_data_account
from django.utils.crypto import get_random_string

User = get_user_model()


def index_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password']
        login_user = authenticate(request, username=password, password=password)
        if login_user is not None:
            login(request, login_user)
            return HttpResponseRedirect(reverse('client'))
        else:
            return HttpResponseRedirect(reverse('index'))

    context = {
        'form': form
    }

    return render(request, 'lex_pusher/index.html', context)


def client_view(request):
    bust = Bust.objects.filter(client=request.user).first()
    stats = Stat.objects.filter(bust=bust)
    bust_stats = Stat.objects.filter(bust=bust)

    context = {
        'stats_times': [i.time.strftime("%m.%d, %H:%M") for i in stats],
        'stats_values': [i.mmr for i in stats[::-1]],
        'stats_current_values': [i.mmr_current for i in stats[::-1]],
        'bust': bust,
        'bust_stats': bust_stats
    }

    return render(request, 'lex_pusher/client/client_index.html', context)


def buster_view(request):
    if not getattr(request.user, "is_booster", False):
        return HttpResponseRedirect(reverse('to_busters'))

    buster = Buster.objects.filter(booster_acc=request.user).first()
    active_bust = Bust.objects.filter(buster=buster).first()
    punishments = Punish.objects.filter(buster_ident=buster)
    inactive_busts = Bust.get_free()
    all_stat_buster = Stat.objects.filter(buster=buster).count()
    win_stat_buster = Stat.objects.filter(buster=buster)
    n = 0
    for i in win_stat_buster:
        if i.mmr > 0:
            n += 1
    if all_stat_buster > 0:
        winrate = round((n / all_stat_buster)*100)
    else:
        winrate = 0
    active_bust_stats = Stat.objects.filter(bust_id=active_bust.id) if active_bust else None
    form = UploadFileForm(request.POST, request.FILES)

    context = {
        'all_stat': all_stat_buster,
        'win_stat': n,
        'winrate': winrate,
        'inactive_busts': inactive_busts,
        'bust_stats': active_bust_stats,
        'punishments': punishments,
        'active_bust': active_bust,
        'buster': buster,
        'form': form,
    }
    return render(request, 'lex_pusher/buster/buster_index.html', context)


def buster_login_view(request):
    form = LoginBusterForm(request.POST or None)
    if form.is_valid():
        login_user = authenticate(request,
                                  username=form.cleaned_data['username'],
                                  password=form.cleaned_data['password'])
        if login_user is not None:
            login(request, login_user)
            return HttpResponseRedirect(reverse('buster'))

    context = {
        'form': form
    }
    return render(request, 'lex_pusher/buster/buster_login.html', context)


def buster_register_view(request):
    form = BusterApplicationForm(request.POST or None)
    if form.is_valid():
        new_buster_application = form.save(commit=False)
        new_buster_application.booster_acc = None
        new_buster_application.save()
        return render(request, 'lex_pusher/buster/buster_register_end.html')

    context = {
        'form': form,
    }
    return render(request, 'lex_pusher/buster/buster_register.html', context)


def accs_shop_view(request):
    accounts = Account.objects.filter(available=True)
    context = {
        'accounts': accounts,
    }
    return render(request, 'lex_pusher/accs/shop_index.html', context)


def bust_shop_view(request):
    return render(request, 'lex_pusher/client/bust_shop_start.html')


def calibration_view(request):
    return render(request, 'lex_pusher/client/calibration_shop.html', {})


def accs_shop_cart_view(request, account_slug):
    account = Account.objects.get(slug=account_slug)
    form = ShopCartForm()

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'lex_pusher/accs/shop_cart.html', context)


def acc_shop_end_view(request):
    account_slug = request.POST.get("account_slug", None)
    account = Account.objects.get(slug=account_slug)
    form = ShopCartForm(request.POST or None)
    if form.is_valid():
        new_purchase_account = form.save(commit=False)
        new_purchase_account.account_slug = account.slug
        new_purchase_account.save()
        description = f'Account|{account.slug},{new_purchase_account.email}'
        fk_url = utils.fk_url(account.price, description)
        return HttpResponseRedirect(fk_url)
    else:
        return HttpResponseRedirect(reverse("cart_account"))


def bust_shop_cart_view(request):
    form_bust = BustCartForm()
    form_acc = ClientForm()
    mmr_from = request.POST.get("mmr_from", None)
    mmr_to = request.POST.get("mmr_to", None)
    price = request.POST.get("price", None)
    type_boost = request.POST.get("type_boost", None)
    if type_boost == "on":
        type_boost = "Support"
    else:
        type_boost = "Core"

    context = {
        'form': form_bust,
        'form_acc': form_acc,
        'mmr_from': mmr_from,
        'mmr_to': mmr_to,
        'type_boost': type_boost,
        'price': price
    }
    return render(request, 'lex_pusher/client/bust_shop_form.html', context)


def bust_confirm_view(request):
    form_bust = BustCartForm(request.POST or None)
    form_acc = ClientForm(request.POST or None)
    mmr_from = request.POST.get("mmr_from", None)
    mmr_to = request.POST.get("mmr_to", None)
    price = request.POST.get("price", None)
    type_boost = request.POST.get("type_boost", None)

    if type_boost == "on":
        type_boost = "Support"
    else:
        type_boost = "Core"

    if form_bust.is_valid() and form_acc.is_valid():
        email = form_acc.cleaned_data['email']
        vk = form_acc.cleaned_data['vk']
        skype = form_acc.cleaned_data['skype']
        phone = form_acc.cleaned_data['phone']
        steam_login = form_bust.cleaned_data['steam_login']
        steam_password = form_bust.cleaned_data['steam_password']
        secret_key = get_random_string(length=10)

        User.objects.create_user(
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

        bust = Bust.objects.create(
            client=request.user,
            mmr_from=mmr_from,
            mmr_to=mmr_to,
            mmr_current=mmr_from,
            mmr_type=type_boost,
            steam_login=steam_login,
            steam_password=steam_password
        )

        logout(request)
        description = f'Boost|{str(bust.id)}'
        fk_url = utils.fk_url(price, description)
        return HttpResponseRedirect(fk_url)


def accs_id_view(request, account_id):
    account = Account.objects.filter(id=account_id)
    context = {
        'account': account
    }
    return render(request, 'lex_pusher/accs/shop_account.html', context)


def pay_success(request):
    price = request.GET.get('AMOUNT' or None)
    description = request.GET.get('MERCHANT_ORDER_ID' or None)
    sign = request.GET.get('SIGN' or None)

    hashes = utils.fk_hash(price, description, True)
    if sign != hashes:
        return HttpResponse("Error")

    pay_for, data = description.split("|")

    if pay_for == 'Boost':
        bust = Bust.objects.get(id=int(data))
        client = bust.client

        secret_key = client.username
        bust.is_paid = True
        bust.save()
        send(client.email, secret_key)

        login_user = authenticate(username=secret_key, password=secret_key)
        if login_user:
            login(request, login_user)

        return HttpResponseRedirect(reverse('index'))

    if pay_for == 'Account':
        slug, email = data.split(",")
        account = Account.objects.get(slug=slug)

        account.available = False
        account.save()
        buyer = BuyAccount.objects.get(account_slug=slug)
        send_data_account(buyer.email, account.steam_login, account.steam_password,
                          account.email_login. account.email_password)
        return HttpResponseRedirect(reverse('index'))

    if pay_for == "Calibration":
        bust = Bust.objects.get(id=int(data))
        client = bust.client

        secret_key = client.username
        bust.is_paid = True
        bust.save()
        send(client.email, secret_key)

        login_user = authenticate(username=secret_key, password=secret_key)
        if login_user:
            login(request, login_user)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def new_stat_view(request):
    mmr = request.POST.get("mmr", "")
    screen = request.POST.get("screen", "")
    buster = Buster.objects.filter(booster_acc=request.user).first()
    active_bust = Bust.objects.filter(buster=buster).first()

    current = active_bust.mmr_current
    Bust.objects.filter(buster=buster).update(mmr_current=current + int(mmr))

    Stat.objects.create(
        bust=active_bust,
        buster=buster,
        mmr=mmr,
        mmr_current=current + int(mmr),
        screen=screen
    )
    return HttpResponseRedirect(reverse('buster'))


def buster_info_change_view(request):
    about_info = request.POST.get("about_yourself", None)
    mmr = request.POST.get("mmr_main", None)
    buster = Buster.objects.filter(booster_acc=request.user)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                avatar = form.clean_avatar()
            except:
                pass
            else:
                instance = Buster(avatar=avatar)
                instance.save()
                buster.update(avatar=avatar)

    if mmr is not None:
        buster.update(solo_mmr=mmr)

    if about_info is not None:
        buster.update(experience=about_info)
    return HttpResponseRedirect(reverse('buster'))


def bust_info_view(request, bust_id):
    buster = Buster.objects.filter(booster_acc=request.user).first()
    found_busts = Bust.objects.filter(id=bust_id).first()
    active_bust = Bust.objects.filter(buster=buster).first()
    found_bust_stats = Stat.objects.filter(bust_id=found_busts.id)
    len_pass = 7 * '*'
    len_login = 7 * '*'
    try:
        if found_busts.mmr_current == 0 or found_busts.mmr_current is None:
            found_busts.mmr_current = found_busts.mmr_from
    except AttributeError:
        print("Nothing")

    context = {
        'found_bust': found_busts,
        'buster': buster,
        'len_pass': len_pass,
        'len_login': len_login,
        'found_bust_stats': found_bust_stats,
        'active_bust': active_bust
    }
    return render(request, 'lex_pusher/buster/bust_info.html', context)


def take_bust_view(request, bust_id):
    buster = Buster.objects.filter(booster_acc=request.user).first()
    taken_bust = Bust.objects.filter(id=bust_id)
    taken_bust.update(buster=buster)
    return HttpResponseRedirect(reverse('buster'))


def calibration_cart_view(request):
    mmr = request.POST.get("mmr", None)
    price = request.POST.get("price", None)
    form_bust = BustCartForm()
    form_acc = ClientForm()

    context = {
        'form_bust': form_bust,
        'form_acc': form_acc,
        'mmr': mmr,
        'price': price
    }
    return render(request, 'lex_pusher/client/calibration_confirm_form.html', context)


def calibration_cart_end_view(request):
    mmr = request.POST.get("mmr", None)
    price = request.POST.get("price", None)
    form_bust = BustCartForm(request.POST or None)
    form_acc = ClientForm(request.POST or None)

    if form_bust.is_valid() and form_acc.is_valid():
        email = form_acc.cleaned_data['email']
        vk = form_acc.cleaned_data['vk']
        skype = form_acc.cleaned_data['skype']
        phone = form_acc.cleaned_data['phone']
        steam_login = form_bust.cleaned_data['steam_login']
        steam_password = form_bust.cleaned_data['steam_password']
        secret_key = get_random_string(length=10)
        type_boost = "Калибровка"

        User.objects.create_user(
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

        bust = Bust.objects.create(
            client=request.user,
            mmr_from=mmr,
            mmr_to=mmr,
            mmr_current=mmr,
            mmr_type=type_boost,
            steam_login=steam_login,
            steam_password=steam_password
        )

        logout(request)
        description = f'Calibration|{str(bust.id)}'
        fk_url = utils.fk_url(price, description)
        return HttpResponseRedirect(fk_url)
    else:
        return HttpResponseRedirect('calibration_cart')


class CeoView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(MyView, self).get_context_data(self, **kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context

    def post(self, request, account_slug):
        template = 'lex_pusher/accs/shop_index.html'
        post = Account.objects.get(slug=account_slug)

        context = {'post': post, 'meta': post.as_meta()}
        return render(request, template, context)


def payout_view(request, id):
    buster = Buster.objects.get(id=id)
    context = {}
    if buster.balance > 500:
        context = {'name': buster.name}
        send_payout('bndr.nkt.99@gmail.com', buster.name, id)
    return render(request, 'lex_pusher/buster/payout.html', context)


def buster_logout(request):
    buster_account = Buster.objects.filter(booster_acc=request.user).first()
    bust = Bust.objects.get(buster=buster_account)
    bust.buster = None
    bust.save()
    return HttpResponseRedirect(reverse("buster"))

