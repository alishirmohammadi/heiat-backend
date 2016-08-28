# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0012_auto_20160828_0743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='additionalObject',
            new_name='additionalOption',
        ),
    ]
