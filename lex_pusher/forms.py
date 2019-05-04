from django import forms
from django.utils import timezone
from .models import BuyAccount, Client
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
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    mmr_from = forms.IntegerField(widget=forms.HiddenInput, disabled=True, required=False)
    mmr_to = forms.IntegerField(widget=forms.HiddenInput, disabled=True, required=False)
    skype = forms.CharField(required=False)
    vk = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = {
            'mmr_from',
            'mmr_to',
            'email',
            'login',
            'password',
            'vk',
            'skype',
            'phone'
        }

    def __init__(self, *args, **kwargs):
        super(BoostCartForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = "Ваш E-Mail"
        self.fields['login'].label = "Логин от Steam"
        self.fields['password'].label = "Пароль от Steam"
        self.fields['vk'].label = "VK"
        self.fields['skype'].label = "Skype"
        self.fields['phone'].label = "Мобильный телефон"
