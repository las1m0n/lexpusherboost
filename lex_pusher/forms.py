from django import forms
from .models import BuyAccount, Bust, Buster, Stat
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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

    class Meta:
        model = Bust
        fields = {
            'mmr_from',
            'mmr_to',
            'steam_login',
            'steam_password'
        }

    def __init__(self, *args, **kwargs):
        super(BoostCartForm, self).__init__(*args, **kwargs)

        self.fields['steam_login'].label = "Логин от Steam"
        self.fields['steam_password'].label = "Пароль от Steam"


class ClientForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput)
    skype = forms.CharField(required=False)
    vk = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    username = forms.CharField(required=False, widget=forms.HiddenInput)
    password1 = forms.CharField(required=False, widget=forms.HiddenInput)
    password2 = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = CustomUser
        fields = {
            'username',
            'password1',
            'password2',
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


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'vk', 'skype', 'phone')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = {
            'password',
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['password'].label = 'PIN-CODE'

    def clean(self):
        password = self.cleaned_data['password']
        user = CustomUser.objects.get(password=password)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')
