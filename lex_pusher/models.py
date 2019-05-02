from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


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
        return "{0} solo {1}, party {2}".format(self.title, self.solo_mmr, self.party_mmr)


class BuyAccount(models.Model):
    account_slug = models.SlugField(default="acc 322")
    email = models.CharField(max_length=120)
    skype = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

    def __str__(self):
        return "Аккаунт {0} куплен с email-> {1}, skype-> {2}, phone-> {3}".\
            format(self.account_slug, self.email, self.skype, self.phone)


class Boost(models.Model):
    mmr_from = models.IntegerField()
    mmr_to = models.IntegerField()
    email = models.EmailField
    login = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    more_info = models.BooleanField(blank=True, null=True)
    vk = models.CharField(max_length=120)
    skype = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

    def __str__(self):
        return "Забустить c {0} mmr по {1} mmr, Логин '{2}' + пароль '{3}' ,куплен с email-> {4}".\
            format(self.mmr_from, self.mmr_to, self.login, self.password, self.email)
