# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-26 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0009_auto_20160824_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='emailPassword',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]