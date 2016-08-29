# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0014_auto_20160828_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='management',
            name='comment',
            field=models.CharField(max_length=800, null=True, blank=True),
        ),
    ]
