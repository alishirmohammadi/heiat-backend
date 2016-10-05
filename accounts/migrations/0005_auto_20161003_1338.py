# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-03 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20161003_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='people_type',
            field=models.CharField(choices=[('sharif student', 'دانشجو شریف'), ('sharif graduated', 'فارغ التحصیل شریف'), ('sharif graduated talabe', 'فاغ التحصیل شریف و طلبه فعلی'), ('sharif graduated student not sharif', 'فارغ التحصیل شریف و دانشجو سایر'), ('not sharif student', 'دانشجو سایر'), ('not sharif graduated', 'فارغ التحصیل سایر'), ('talabe', 'طلبه'), ('sharif master', 'استاد شریف'), ('sharif employed', 'کارمند شریف'), ('other', 'سایر')], default='other', max_length=200, verbose_name='وضعیت تحصیل'),
        ),
    ]