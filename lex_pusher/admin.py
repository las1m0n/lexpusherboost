from django.contrib import admin
from .models import Account, BuyAccount, Boost

admin.site.register(Account)
admin.site.register(BuyAccount)
admin.site.register(Boost)
