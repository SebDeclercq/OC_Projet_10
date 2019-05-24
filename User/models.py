from typing import List
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email: models.EmailField = models.EmailField(
        _('email address'), max_length=255, unique=True
    )
    firstname: models.CharField = models.CharField(
        _('first name'), max_length=255, blank=True
    )
    name: models.CharField = models.CharField(
        _('last name'), max_length=255, blank=True
    )
    is_active: models.BooleanField = models.BooleanField(
        _('active'), default=True
    )
    is_staff: models.BooleanField = models.BooleanField(
        _('staff'), default=False
    )

    objects: UserManager = UserManager()

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELD: List[str] = []

    class Meta:
        verbose_name: str = _('user')
        verbose_name_plural: str = _('users')

    def get_full_name(self) -> str:
        return format_lazy('{firstname} {name}', firstname=self.firstname,
                           name=self.name).strip()
