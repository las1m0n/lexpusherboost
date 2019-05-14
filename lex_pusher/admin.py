from django.contrib import admin
from .models import Account, BuyAccount, Buster, Bust, Stat
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm
from users.models import CustomUser

admin.site.site_header = "FLEX PUSHER ADMIN PANEL"

admin.site.register(Account)
admin.site.register(BuyAccount)
admin.site.register(Buster)
admin.site.register(Bust)
admin.site.register(Stat)
