from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import BuyAccount, Bust, Buster, Calibration
from django.core.files.images import get_image_dimensions
from django.core.validators import FileExtensionValidator
User = get_user_model()


class ShopCartForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    skype = forms.CharField(required=False)
    phone = forms.CharField(required=False)

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


class CalibrationCartForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    mmr = forms.CharField(required=False, widget=forms.HiddenInput)
    price = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Calibration
        fields = {
            'email',
            'steam_login',
            'steam_password',
            'mmr',
            'price',
        }

    def __init__(self, *args, **kwargs):
        super(CalibrationCartForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = "E-Mail"
        self.fields['steam_login'].label = "Steam Логин"
        self.fields['steam_password'].label = "Steam Пароль"


class BustCartForm(forms.ModelForm):
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
        super(BustCartForm, self).__init__(*args, **kwargs)

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
        model = User
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


class LoginForm(forms.ModelForm):
    password = forms.CharField(min_length=6, max_length=32,
                               widget=forms.PasswordInput(attrs={'humanReadable': 'Пароль'}), label='Пароль')

    class Meta:
        model = User
        fields = {
            'password',
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['password'].label = 'PIN-CODE'

    def clean(self):
        if not self._errors:
            cleaned_data = super(LoginForm, self).clean()
            password = cleaned_data.get('password')
            try:
                user = User.objects.get(username=password)
                if not user.check_password(password):
                    raise forms.ValidationError(u'Неверный пароль')
                elif not user.is_active:
                    raise forms.ValidationError(u'Пользователь с таким паролем заблокирован.')
            except User.DoesNotExist:
                raise forms.ValidationError(u'Такого буста не существует.')
            return cleaned_data


class LoginBusterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=120)

    class Meta:
        username = forms.CharField(required=False)
        password = forms.PasswordInput()
        model = User
        fields = {
            'username',
            'password',
        }

    def __init__(self, *args, **kwargs):
        super(LoginBusterForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Пароль'
        self.fields['username'].label = 'Логин'

    def clean(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        if password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Неверный пароль или логин!')


class BusterApplicationForm(forms.ModelForm):
    class Meta:
        model = Buster
        fields = {
            'name',
            'phone',
            'email',
            'skype',
            'vk',
            'wmr',
            'solo_mmr',
            'experience'
        }

    def __init__(self, *args, **kwargs):
        super(BusterApplicationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Имя Фамилия"
        self.fields['phone'].label = "Номер телефона"
        self.fields['email'].label = "Email"
        self.fields['skype'].label = "Skype"
        self.fields['wmr'].label = "WMR кошелек"
        self.fields['solo_mmr'].label = "Текущий соло ммр"
        self.fields['experience'].label = "О своих навыках"


class UploadFileForm(forms.Form):
    file = forms.FileField(required=False, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

        self.fields['file'].label = "Аватар"

    def clean_avatar(self):
        avatar = self.cleaned_data['file']

        try:
            w, h = get_image_dimensions(avatar)
            max_width = max_height = 129
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
