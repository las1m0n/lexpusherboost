from __future__ import unicode_literals
from django.db import models
import uuid
from django.urls import reverse
from decimal import Decimal
from django.db.models.signals import pre_save


def image_folder(instance, filename):
    filename = instance.slug + "." + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Account(models.Model):
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
    account_slug = models.SlugField(default="acc 322")
    email = models.CharField(max_length=120)
    skype = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

    def __str__(self):
        return f"Аккаунт {self.account_slug} куплен с email-> {self.email}, skype-> {self.skype}, " \
            f"phone-> {self.phone}"


class Client(models.Model):
    slug = models.SlugField(blank=True, default="model")

    password = models.CharField(max_length=120, default="password")

    vk = models.CharField(max_length=120, default="VK", null=True, blank=True)
    skype = models.CharField(max_length=120, default="Skype", null=True, blank=True)
    phone = models.CharField(max_length=120, default="PHONE", null=True, blank=True)
    email = models.EmailField(default="0@gmail.com")

    def __str__(self):
        return f"Клиент {self.slug} с email-> {self.email}, skype-> {self.skype}, phone-> {self.phone}"

    def slug_create(self):
        return f"{self.email} + skype {self.skype} + phone {self.phone}"


def pre_save_client_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = str(instance.slug_create())
        instance.slug = slug


pre_save.connect(pre_save_client_slug, sender=Client)


class Buster(models.Model):
    slug = models.SlugField(blank=True, default="cebek")

    password = models.CharField(max_length=120)
    email = models.EmailField(default="0@gmail.com")


class Bust(models.Model):
    slug = models.SlugField(blank=True, null=True, default="cebek")

    client_slug = models.ForeignKey(Client, True, null=True)
    buster_slug = models.ForeignKey(Buster, True, null=True)

    mmr_from = models.IntegerField()
    mmr_to = models.IntegerField()

    steam_login = models.CharField(max_length=120)
    steam_password = models.CharField(max_length=120)

    def __str__(self):
        return f"Забустить c {self.mmr_from} mmr по {self.mmr_to} mmr, " \
                   f"Логин '{self.steam_login}' + пароль '{self.steam_password}'"

    def slug_create(self):
        return f"Boost {self.mmr_from} -> {self.mmr_to} login {self.steam_login}"


def pre_save_bust_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = str(instance.slug_create())
        instance.slug = slug


pre_save.connect(pre_save_bust_slug, sender=Bust)


class Stats:
    pass
#     bust_id = models.ForeignKey(Bust, True)
#
#     match_id = models.IntegerField(primary_key=True)
#     mmr = models.FloatField()
#     is_win = models.BooleanField()
#     time = models.TimeField()














