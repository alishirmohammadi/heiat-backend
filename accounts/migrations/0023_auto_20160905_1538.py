# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-05 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20160905_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='profile'),
        ),
    ]
