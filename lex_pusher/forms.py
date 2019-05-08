from django import forms
from django.utils import timezone
from .models import BuyAccount, Client, Bust, Buster, Stats
from django.contrib.auth.models import User


class ShopCartForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)

    class Meta:
        model = BuyAccount
        fields = {
            'email',
            'skype',
            'phone'
        }

    def __init__(self, *args, **kwargs):
        super(ShopCartForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = "Ваш E-Mail"
        self.fields['skype'].label = "Skype"
        self.fields['phone'].label = "Телефон"


class BoostCartForm(forms.ModelForm):
    steam_password = forms.CharField(widget=forms.PasswordInput)
    mmr_from = forms.IntegerField(widget=forms.HiddenInput, disabled=True, required=False)
    mmr_to = forms.IntegerField(widget=forms.HiddenInput, disabled=True, required=False)
    slug = forms.SlugField(widget=forms.HiddenInput, disabled=True, required=False)

    class Meta:
        model = Bust
        fields = {
            'slug',
            'mmr_from',
            'mmr_to',
            'steam_login',
            'steam_password'
        }

    def __init__(self, *args, **kwargs):
        super(BoostCartForm, self).__init__(*args, **kwargs)

        self.fields['steam_login'].label = "Логин от Steam"
        self.fields['steam_password'].label = "Пароль от Steam"


class ClientForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    skype = forms.CharField(required=False)
    vk = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = {
            'email',
            'skype',
            'vk',
            'phone'
        }

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = "Email"
        self.fields['skype'].label = "Skype"
        self.fields['vk'].label = "VK id"
        self.fields['phone'].label = "Phone"

