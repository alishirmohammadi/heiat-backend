# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-19 04:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('program', '0003_auto_20160819_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberOfInstallment', models.IntegerField(default=1)),
                ('amount', models.IntegerField()),
                ('refId', models.CharField(blank=True, max_length=40, null=True)),
                ('saleRefId', models.CharField(blank=True, max_length=40, null=True)),
                ('takingDate', models.DateTimeField(default=datetime.datetime.now)),
                ('success', models.BooleanField(default=False)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.Registration')),
            ],
        ),
    ]
