from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_client', True)
        extra_fields.setdefault('is_booster', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_client', False)
        extra_fields.setdefault('is_booster', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email")
    username = models.CharField(unique=True, max_length=120, verbose_name="Ключ")
    vk = models.CharField(max_length=120, default="VK", null=True, blank=True)
    skype = models.CharField(max_length=120, default="Skype", null=True, blank=True)
    phone = models.CharField(max_length=120, default="PHONE", null=True, blank=True)

    is_booster = models.BooleanField(_('booster status'),
                                     default=False,
                                     help_text=_('Booster Status Resistance'), )
    is_client = models.BooleanField(_('client status'),
                                    default=False,
                                    help_text=_('Client Status Resistance'), )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
