from .models import Account, BuyAccount, Buster, Bust, Stat, Punish
from django.contrib import admin
from django.db.models import F

from .models import Account, BuyAccount, Buster, Bust, Stat, Punish, Calibration

admin.site.site_header = "FLEX PUSHER ADMIN PANEL"

admin.site.register(Account)
admin.site.register(BuyAccount)
admin.site.register(Buster)
admin.site.register(Bust)
admin.site.register(Stat)
admin.site.register(Calibration)


def make_published(modeladmin, request, queryset):
    for q in queryset:
        buster = Buster.objects.filter(id=q.buster_ident.id)
        for item in buster:
            if item.balance >= q.cost:
                buster.update(balance=F('balance') - q.cost)


make_published.short_description = "Применить штраф"


class PunishAdmin(admin.ModelAdmin):
    actions = [make_published]


admin.site.register(Punish, PunishAdmin)
