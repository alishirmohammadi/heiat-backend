# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-22 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160819_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='passport',
            field=models.CharField(choices=[('have', 'دارم'), ('have 7', 'دارم ولی کمتر از 7 ماه انقضا دارد '), ('not have', 'ندارم')], max_length=200, null=True),
        ),
    ]
