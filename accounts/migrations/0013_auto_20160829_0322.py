# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20160828_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='passport',
            field=models.CharField(max_length=200, null=True, choices=[(b'have', b'\xd8\xaf\xd8\xa7\xd8\xb1\xd9\x85'), (b'not have', b'\xd9\x86\xd8\xaf\xd8\xa7\xd8\xb1\xd9\x85')]),
        ),
    ]
