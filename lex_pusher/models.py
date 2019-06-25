from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from datetime import datetime


def image_folder(instance, filename):
    filename = instance.slug + "." + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Account(models.Model):
    class Meta:
        verbose_name = 'Буст'
        verbose_name_plural = 'Аккаунты на продажу'

    title = models.CharField(max_length=120)
    solo_mmr = models.CharField(max_length=120)
    party_mmr = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} solo {self.solo_mmr}, party {self.party_mmr}"


class BuyAccount(models.Model):

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Покупатели аккаунтов готовых'

    account_slug = models.SlugField(primary_key=True)
    email = models.CharField(max_length=120)
    skype = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

    def __str__(self):
        return f"Аккаунт {self.account_slug} куплен с email-> {self.email}, skype-> {self.skype}, " \
            f"phone-> {self.phone}"


class Buster(models.Model):

    class Meta:
        verbose_name = 'Заявка на бустера'
        verbose_name_plural = 'Заявки на бустера'

    booster_acc = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField()
    vk = models.CharField(max_length=120, blank=True, null=True)
    skype = models.CharField(max_length=120, blank=True, null=True)
    wmr = models.CharField(max_length=120, blank=True, null=True)
    solo_mmr = models.IntegerField(default=1)
    experience = models.TextField(default="Nothing")

    def __str__(self):
        return f"Заявка на бустера {self.id}, {self.name} и с email-> {self.email}"


class Punish(models.Model):

    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'

    buster_ident = models.ForeignKey(Buster, on_delete=models.CASCADE, blank=True, null=True)
    cost = models.IntegerField(default=0)
    reason = models.TextField(default="Бан по причине")


class Bust(models.Model):

    class Meta:
        verbose_name = 'Буст'
        verbose_name_plural = 'Бусты'

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    buster_id = models.ForeignKey(Buster, True, null=True)
    mmr_from = models.IntegerField()
    mmr_to = models.IntegerField()

    steam_login = models.CharField(max_length=120)
    steam_password = models.CharField(max_length=120)

    start_date = models.DateField(default=datetime.now)

    @classmethod
    def get_inactive(cls):
        return cls.objects.filter(buster_id=None)

    def __str__(self):
        return f"{self.id} Забустить c {self.mmr_from} mmr по {self.mmr_to} mmr, " \
                   f"Логин '{self.steam_login}' + пароль '{self.steam_password}'"


class Stat(models.Model):
    class Meta:
        verbose_name = 'Стат'
        verbose_name_plural = 'Статы'

    bust_id = models.ForeignKey(Bust, True)
    match_id = models.IntegerField(null=True)
    mmr = models.FloatField()
    time = models.DateTimeField()

    @property
    def is_win(self):
        return self.mmr > 0
