from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    vk = models.CharField(max_length=120, default="VK", null=True, blank=True)
    skype = models.CharField(max_length=120, default="Skype", null=True, blank=True)
    phone = models.CharField(max_length=120, default="PHONE", null=True, blank=True)
    email = models.EmailField(default="0@gmail.com")

    def __str__(self):
        return f"Клиент {self.id} с email-> {self.email}, skype-> {self.skype}, phone-> {self.phone}"
