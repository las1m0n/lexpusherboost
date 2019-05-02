from django import forms
from django.utils import timezone
from .models import BuyAccount, Boost
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
        self.fields['email'].help_text = "E-Mail"
        self.fields['skype'].label = "Skype"
        self.fields['skype'].help_text = "Логин Skype"
        self.fields['phone'].label = "Телефон"
        self.fields['phone'].help_text = "8 (999) 123 45 67"


class BoostCartForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Boost
        fields = {
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
        self.fields['email'].help_text = "E-Mail"
        self.fields['login'].label = "Логин от Steam"
        self.fields['login'].help_text = "Steam логин"
        self.fields['password'].label = "Пароль от Steam"
        self.fields['password'].help_text = "svindura"
        self.fields['vk'].label = "VK"
        self.fields['vk'].help_text = "id3221488"
        self.fields['skype'].label = "Skype"
        self.fields['skype'].help_text = "Логин Skype"
        self.fields['phone'].label = "Телефон"
        self.fields['phone'].help_text = "8 (999) 123 45 67"
