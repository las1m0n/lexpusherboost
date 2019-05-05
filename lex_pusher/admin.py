from django.contrib import admin
from .models import Account, BuyAccount, Client

admin.site.site_header = "FLEX PUSHER ADMIN PANEL"

admin.site.register(Account)
admin.site.register(BuyAccount)
admin.site.register(Client)
