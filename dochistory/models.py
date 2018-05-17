from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from editor.models import Doc
# Create your models here.
class DocHistory(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('Дата добавления'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'))
    doc = models.ForeignKey(Doc, verbose_name=_('Документ'))
    previous_version = models.TextField(_('Предыдущая версия'))
