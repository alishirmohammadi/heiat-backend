# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-09-03 14:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0004_expense_callback_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': 'درگاه', 'verbose_name_plural': 'درگاه\u200cها'},
        ),
    ]