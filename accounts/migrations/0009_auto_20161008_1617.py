# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-08 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20161005_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='couple',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile', verbose_name='همسر'),
        ),
    ]
