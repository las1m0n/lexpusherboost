# from django import forms
# from django.utils import timezone
# from django.contrib.auth.models import User
#
#
# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     password_check = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = {
#             'username',
#             'password',
#             'password_check',
#             'first_name',
#             'last_name',
#             'email'
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#
#         self.fields['username'].label = "Имя Пользователя"
#         self.fields['password'].label = "Пароль"
#         self.fields['password'].help_text = "Придумайте Пароль"
#         self.fields['password_check'].label = "Повторите пароль"
#         self.fields['first_name'].label = "Введите Имя"
#         self.fields['last_name'].label = "Введите Фамилию"
#         self.fields['email'].label = "Ваша почта"
#         self.fields['email'].help_text = "Пожалуйста, указывайте реальный адрес электронной почты"
#
#     def clean(self):
#         username = self.cleaned_data['username']
#         password = self.cleaned_data['password']
#         password_check = self.cleaned_data['password_check']
#         email = self.cleaned_data['email']
#
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован.')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('Пользователь с данным e-mail уже зарегистрирован.')
#         if password != password_check:
#             raise forms.ValidationError('Пароли не совпадают')