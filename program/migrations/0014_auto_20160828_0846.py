# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0013_auto_20160828_0831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricing',
            old_name='additionalObject',
            new_name='additionalOption',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='additionalObject',
            new_name='additionalOption',
        ),
    ]
