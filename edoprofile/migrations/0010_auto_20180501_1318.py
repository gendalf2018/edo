# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-01 13:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edoprofile', '0009_edouser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edouser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='edouser',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='EdoUser',
        ),
    ]
