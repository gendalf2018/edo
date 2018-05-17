from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils import timezone

class Doc(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('Дата добавления'))
    date_updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_('Дата обновления'))
    name = models.CharField(_('Название'), max_length=300, default="no_name")
    html = models.TextField(_('Содержимое документа'))
    u_group = models.ManyToManyField(Group, blank=True, verbose_name=_('Группа'))
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name=_('Пользователь'))

    def __str__(self):
        return self.name
    def get_short_name(self):
        if len(self.name) < 20:
            return self.name
        return self.name[0:35] + '...'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('editorurl', kwargs={'pk': str(self.pk)})
