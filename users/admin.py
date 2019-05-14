from django.contrib import admin

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from lex_pusher.forms import ClientForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = ClientForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'password']


admin.site.register(CustomUser, CustomUserAdmin)
