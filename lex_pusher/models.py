from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.db import models
from meta.models import ModelMeta


def image_folder(instance, filename):
    filename = instance.slug + "." + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


def image_buster_folder(instance, filename):
    filename = instance.name + "." + filename.split('.')[1]
    return "{0}/{1}".format(instance.name, filename)


class Account(ModelMeta, models.Model):
    class Meta:
        verbose_name = 'Буст'
        verbose_name_plural = 'Аккаунты на продажу'

    title = models.CharField(max_length=120)
    core_mmr = models.CharField(max_length=120)
    support_mmr = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    dotabuff = models.CharField(max_length=120)
    steam_acc = models.CharField(max_length=120)
    image_avatar = models.ImageField(upload_to=image_folder)
    image_main = models.ImageField(upload_to=image_folder)
    price = models.PositiveIntegerField(default=10)
    available = models.BooleanField(default=True)
    email_password = models.CharField(max_length=120)
    email_login = models.CharField(max_length=120)
    steam_password = models.CharField(max_length=120)
    steam_login = models.CharField(max_length=120)

    _metadata = {
        'title': 'title',
        'description': 'description',
        'image': 'get_meta_image',
    }

    def __str__(self):
        return f"{self.title} core {self.core_mmr}, core {self.support_mmr}"

    def get_meta_image(self):
        if self.image:
            return self.image.url


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
    avatar = models.ImageField(upload_to='', default='dota-2.png', blank=True, null=True)
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

    def __str__(self):
        return f"{self.id} Штраф {self.buster_ident} на {self.cost} рублей"


class Bust(models.Model):
    class Meta:
        verbose_name = 'Буст'
        verbose_name_plural = 'Бусты'

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    buster = models.ForeignKey(Buster, True, null=True)

    mmr_from = models.IntegerField()
    mmr_to = models.IntegerField()
    mmr_current = models.IntegerField()
    mmr_type = models.CharField(default="none", max_length=120)

    steam_login = models.CharField(max_length=120)
    steam_password = models.CharField(max_length=120)

    is_paid = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.now)

    @classmethod
    def get_free(cls):
        return cls.objects.filter(buster=None, is_paid=True)

    @property
    def mmr_left(self):
        return self.mmr_to - self.mmr_current

    def __str__(self):
        return f"{self.id} Забустить c {self.mmr_from} mmr по {self.mmr_to} mmr, " \
            f"Логин '{self.steam_login}' + пароль '{self.steam_password}'"


class Stat(models.Model):
    class Meta:
        verbose_name = 'Стат'
        verbose_name_plural = 'Статы'

    bust = models.ForeignKey(Bust, True)
    buster = models.ForeignKey(Buster, True)
    screen = models.CharField(max_length=255)
    mmr = models.IntegerField()
    mmr_current = models.IntegerField(default=0)
    time = models.DateTimeField(default=datetime.now)

    @property
    def is_win(self):
        return self.mmr > 0

    def __str__(self):
        return f"буст ид: {self.bust.id}  ммр: {self.mmr}"


class Calibration(models.Model):
    class Meta:
        verbose_name = 'Калибровка'
        verbose_name_plural = 'Калибровки'

    email = models.EmailField(max_length=120)
    steam_password = models.CharField(max_length=120)
    steam_login = models.CharField(max_length=120)
    price = models.PositiveIntegerField(default=0)
    mmr = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Калибровка куплена с email-> {self.email}, mmr-> {self.mmr}, " \
            f"за  {self.price}"