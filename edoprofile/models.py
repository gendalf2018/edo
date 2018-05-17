# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.gis.db.models import signals as signals
from django.dispatch.dispatcher import receiver

from colorfield.fields import ColorField

class EdoUserManager(UserManager):

    def create_user(self, email, password=None):
        username = email
        return super(EdoUserManager, self).create_user(self, username, email, password)

    def create_superuser(self, email, password):
        username = email
        return super(EdoUserManager, self).create_superuser(self, email, password)




class EdoUser(AbstractUser):
    username = models.CharField(_('Имя пользователя'), max_length=255, blank=True, null=True)
    email = models.EmailField(
        _('E-mail'),
        max_length=255,
        unique=True,
    )
    occupation = models.CharField(_('Должность'), max_length=300, blank=True)
    father_name = models.CharField(_('Отчество'), max_length=100, blank=True)
    birth_date = models.DateField(_('Дата рождения'), null=True, blank=True)
    ip_address = models.GenericIPAddressField(_('IP адрес'), blank=True, null=True)
    phone = models.CharField(_('Телефон'), blank=True, max_length=15)
    skype = models.CharField(_('Skype'), max_length=100, blank=True)
    address = models.CharField(_('Адрес'), blank=True, null=True, max_length=400)
    color = ColorField(_('Цвет'), default='#FF0000')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'occupation',
        'first_name',
        'last_name',
        'father_name',
        'phone',
        'address'
        ]

    objects = EdoUserManager()

    def __str__(self):
        if self.first_name:
            return self.first_name + ' ' + self.last_name
        return self.email


def create_admin_user(app_config, **kwargs):
    if app_config.name != 'edoprofile':
        return None
    try:
        EdoUser.objects.get(email='admin@localhost')
    except EdoUser.DoesNotExist:
        print('Creating admin user: email: admin@localhost, password: 123')
        assert EdoUser.objects.create_superuser('admin@localhost', '123')
    else:
        print('Admin user already exists')


signals.post_migrate.connect(create_admin_user)
from .signals import *
