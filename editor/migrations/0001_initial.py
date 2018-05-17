# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-09 08:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0010_auto_20180501_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='no_name', max_length=300, verbose_name='Название')),
                ('html', models.TextField(verbose_name='Содержимое документа')),
                ('u_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='Группа')),
            ],
        ),
    ]