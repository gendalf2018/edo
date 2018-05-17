# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class EdoProfileConfig(AppConfig):
    name = 'edoprofile'
    verbose_name = _('Пользователь')

    def ready(self):
        import edoprofile.signals
