from django import forms
from django.utils import timezone
from .models import BuyAccount
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
        self.fields['skype'].label = "Логин Skype"
        self.fields['email'].label = "Телефон"
        self.fields['email'].label = "8 (999) 123 45 67"
