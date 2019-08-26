from django.contrib.sitemaps import Sitemap

from .models import Account, Bust, Calibration


class AccountSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Account.objects.all()
