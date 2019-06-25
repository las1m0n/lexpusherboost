from django.contrib import admin
from .models import Account, BuyAccount, Buster, Bust, Stat, Punish
from django.contrib import admin
from django.db.models import Count, F, Value
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = "FLEX PUSHER ADMIN PANEL"

admin.site.register(Account)
admin.site.register(BuyAccount)
admin.site.register(Buster)
admin.site.register(Bust)
admin.site.register(Stat)


def make_published(modeladmin, request, queryset):
    for q in queryset:
        buster = Buster.objects.filter(id=q.buster_ident.id)
        for item in buster:
            if item.balance >= q.cost:
                buster.update(balance=F('balance')-q.cost)


make_published.short_description = "Применить штраф"


class PunishAdmin(admin.ModelAdmin):
    actions = [make_published]


admin.site.register(Punish, PunishAdmin)
