from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_booster', 'is_client')}),
        (_('Important dates'), {'fields': ('last_login', 'vk')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_booster', 'is_client'),
        }),
    )
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_booster', 'is_client')
    search_fields = ('username', 'email', 'phone', 'is_staff', 'is_booster', 'is_client')


admin.site.register(get_user_model(), UserAdmin)
