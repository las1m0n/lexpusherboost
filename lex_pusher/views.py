import secrets

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from .forms import ShopCartForm, BustCartForm, ClientForm, LoginForm, BusterApplicationForm, LoginBusterForm, \
    UploadFileForm
from .mail_send import send
from . import utils
from .models import Account, Bust, Stat, Buster, Punish
from django.contrib.auth import get_user_model
import json

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
        'stats_values': [i.mmr for i in stats],
        'stats_current_values': [i.mmr_current for i in stats],
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

    active_bust_stats = Stat.objects.filter(bust_id=active_bust.id) if active_bust else None

    form = UploadFileForm(request.POST, request.FILES)

    context = {
        'inactive_busts': inactive_busts,
        'bust_stats': active_bust_stats,
        'punishments': punishments,
        'active_bust': active_bust,
        'buster': buster,
        'form': form
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


def accs_shop_cart_view(request, account_slug):
    account = Account.objects.get(slug=account_slug)
    form = ShopCartForm(request.POST or None)
    if form.is_valid():
        new_purchase_account = form.save(commit=False)
        new_purchase_account.account_slug = account.slug
        new_purchase_account.save()
        return HttpResponseRedirect(reverse('index'))

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'lex_pusher/accs/shop_cart.html', context)


def bust_shop_cart_view(request):
    form_bust = BustCartForm(request.POST or None)
    form_acc = ClientForm(request.POST or None)
    mmr_from = request.GET.get("mmr_from", None)
    mmr_to = request.GET.get("mmr_to", None)
    price = request.GET.get("price", None)

    if form_bust.is_valid() and form_acc.is_valid():
        email = form_acc.cleaned_data['email']
        vk = form_acc.cleaned_data['vk']
        skype = form_acc.cleaned_data['skype']
        phone = form_acc.cleaned_data['phone']
        steam_login = form_bust.cleaned_data['steam_login']
        steam_password = form_bust.cleaned_data['steam_password']
        secret_key = secrets.token_hex(nbytes=8)

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
            steam_login=steam_login,
            steam_password=steam_password
        )

        description = 'bust|' + str(bust.id)
        fk_url = utils.fk_url(price, description)
        return HttpResponseRedirect(fk_url)

    context = {
        'form': form_bust,
        'form_acc': form_acc,
        'mmr_from': mmr_from,
        'mmr_to': mmr_to,
    }
    return render(request, 'lex_pusher/client/bust_shop_form.html', context)


def pay_success(request):
    price = request.POST['AMOUNT']
    description = request.POST['MERCHANT_ORDER_ID']
    sign = request.POST['SIGN']

    hash = utils.fk_hash(price, description, True)
    if sign != hash:
        return HttpResponse("ты че наебать нас вздумал?")

    pay_for, data = description.split("|")

    if pay_for == 'bust':

        bust = Bust.objects.get(id=int(data))
        client = bust.client
        bust.update(is_paid=True)

        secret_key = client.username

        send(client.email, secret_key)

        login_user = authenticate(username=secret_key, password=secret_key)
        if login_user:
            login(request, login_user)

        return HttpResponseRedirect(reverse('client'))

    if pay_for == 'acc':
        pass


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
        bust_id=active_bust,
        mmr=mmr,
        mmr_current=current + int(mmr),
        screen=screen
    )
    return HttpResponseRedirect(reverse('buster_cabinet'))


def buster_info_change_view(request):
    about_info = request.POST.get("about_yourself", None)
    mmr = request.POST.get("mmr_main", None)
    buster = Buster.objects.filter(booster_acc=request.user)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.clean_avatar()
            instance = Buster(avatar=avatar)
            instance.save()
            buster.update(avatar=avatar)

    if mmr is not None:
        buster.update(solo_mmr=mmr)
        buster.save()

    if about_info is not None:
        buster.update(experience=about_info)
        buster.save()
    return HttpResponseRedirect(reverse('buster_cabinet'))


def bust_info_view(request, bust_id):
    buster = Buster.objects.filter(booster_acc=request.user).first()
    found_busts = Bust.objects.filter(id=bust_id).first()
    active_bust = Bust.objects.filter(buster=buster).first()
    found_bust_stats = Stat.objects.filter(bust_id=found_busts.id)
    len_pass = len(found_busts.steam_password) * '*'
    len_login = len(found_busts.steam_login) * '*'
    try:
        if found_busts.mmr_current == 0 or found_busts.mmr_current is None:
            found_busts.mmr_current = found_busts.mmr_from
    except AttributeError:
        print("Nothing")

    context = {
        'found_bust': found_busts,
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
    return HttpResponseRedirect(reverse('buster_cabinet'))


class PayView(TemplateView):
    template_name = 'lex_pusher/buster/buster_payout.html'

    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': '100',
            'currency': 'USD',
            'description': 'Payment for clothes',
            'order_id': 'order_id_2',
            'version': '3',
            'sandbox': 0,
            'server_url': 'https://test.com/billing/pay-callback/',
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        pass


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class AuthorCreate(AjaxableResponseMixin, CreateView):
    model = User
    fields = ['username', 'password']
