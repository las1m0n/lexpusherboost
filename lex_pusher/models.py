from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from users.models import CustomUser
import uuid
from django.urls import reverse
from decimal import Decimal
from django.db.models.signals import pre_save
from datetime import datetime


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
    account_slug = models.SlugField(primary_key=True)
    email = models.CharField(max_length=120)
    skype = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

    def __str__(self):
        return f"Аккаунт {self.account_slug} куплен с email-> {self.email}, skype-> {self.skype}, " \
            f"phone-> {self.phone}"


class Buster(models.Model):
    password = models.CharField(max_length=120)
    email = models.EmailField(default="0@gmail.com")

    def __str__(self):
        return f"Клиент {self.id} с email-> {self.email} and password->{self.password}"


class Bust(models.Model):

    client = models.ForeignKey(CustomUser, True, blank=True, null=True)
    buster_id = models.ForeignKey(Buster, True, null=True)

    mmr_from = models.IntegerField()
    mmr_to = models.IntegerField()

    steam_login = models.CharField(max_length=120)
    steam_password = models.CharField(max_length=120)

    start_date = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.id} Забустить c {self.mmr_from} mmr по {self.mmr_to} mmr, " \
                   f"Логин '{self.steam_login}' + пароль '{self.steam_password}'"


class Stat(models.Model):
    bust_id = models.ForeignKey(Bust, True)

    match_id = models.IntegerField(null=True)
    mmr = models.FloatField()
    time = models.DateTimeField()

