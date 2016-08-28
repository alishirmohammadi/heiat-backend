# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_profile_coupling'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='conscription',
            field=models.CharField(max_length=200, choices=[(b'went', b'\xd8\xaf\xd8\xa7\xd8\xb1\xd8\xa7\xdb\x8c \xda\xa9\xd8\xa7\xd8\xb1\xd8\xaa \xd9\xbe\xd8\xa7\xdb\x8c\xd8\xa7\xd9\x86 \xd8\xae\xd8\xaf\xd9\x85\xd8\xaa'), (b'exempt', b'\xd9\x85\xd8\xb9\xd8\xa7\xd9\x81\xdb\x8c\xd8\xaa \xd8\xaf\xd8\xa7\xdb\x8c\xd9\x85 '), (b'educational exempt', b'\xd9\x85\xd8\xb9\xd8\xa7\xd9\x81\xdb\x8c\xd8\xaa \xd8\xaa\xd8\xad\xd8\xb5\xdb\x8c\xd9\x84\xdb\x8c'), (b'other', b'\xd8\xb3\xd8\xa7\xdb\x8c\xd8\xb1')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='passport',
            field=models.CharField(max_length=200, null=True, choices=[(b'have', b'\xd8\xaf\xd8\xa7\xd8\xb1\xd9\x85'), (b'have 7', b'\xd8\xaf\xd8\xa7\xd8\xb1\xd9\x85 \xd9\x88\xd9\x84\xdb\x8c \xda\xa9\xd9\x85\xd8\xaa\xd8\xb1 \xd8\xa7\xd8\xb2 7 \xd9\x85\xd8\xa7\xd9\x87 \xd8\xa7\xd9\x86\xd9\x82\xd8\xb6\xd8\xa7 \xd8\xaf\xd8\xa7\xd8\xb1\xd8\xaf '), (b'not have', b'\xd9\x86\xd8\xaf\xd8\xa7\xd8\xb1\xd9\x85')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='people_type',
            field=models.CharField(max_length=200, choices=[(b'sharif student', b'\xd8\xaf\xd8\xa7\xd9\x86\xd8\xb4\xd8\xac\xd9\x88 \xd8\xb4\xd8\xb1\xdb\x8c\xd9\x81'), (b'sharif graduated', b'\xd9\x81\xd8\xa7\xd8\xb1\xd8\xba \xd8\xa7\xd9\x84\xd8\xaa\xd8\xad\xd8\xb5\xdb\x8c\xd9\x84 \xd8\xb4\xd8\xb1\xdb\x8c\xd9\x81'), (b'sharif graduated talabe', b'\xd9\x81\xd8\xa7\xd8\xba \xd8\xa7\xd9\x84\xd8\xaa\xd8\xad\xd8\xb5\xdb\x8c\xd9\x84 \xd8\xb4\xd8\xb1\xdb\x8c\xd9\x81 \xd9\x88 \xd8\xb7\xd9\x84\xd8\xa8\xd9\x87 \xd9\x81\xd8\xb9\xd9\x84\xdb\x8c'), (b'sharif graduated student not sharif', b'\xd9\x81\xd8\xa7\xd8\xb1\xd8\xba \xd8\xa7\xd9\x84\xd8\xaa\xd8\xad\xd8\xb5\xdb\x8c\xd9\x84 \xd8\xb4\xd8\xb1\xdb\x8c\xd9\x81 \xd9\x88 \xd8\xaf\xd8\xa7\xd9\x86\xd8\xb4\xd8\xac\xd9\x88 \xd8\xb3\xd8\xa7\xdb\x8c\xd8\xb1'), (b'not sharif student', b'\xd8\xaf\xd8\xa7\xd9\x86\xd8\xb4\xd8\xac\xd9\x88 \xd8\xb3\xd8\xa7\xdb\x8c\xd8\xb1'), (b'not sharif graduated', b'\xd9\x81\xd8\xa7\xd8\xb1\xd8\xba \xd8\xa7\xd9\x84\xd8\xaa\xd8\xad\xd8\xb5\xdb\x8c\xd9\x84 \xd8\xb3\xd8\xa7\xdb\x8c\xd8\xb1'), (b'talabe', b'\xd8\xb7\xd9\x84\xd8\xa8\xd9\x87'), (b'sharif master', b'\xd8\xa7\xd8\xb3\xd8\xaa\xd8\xa7\xd8\xaf \xd8\xb4\xd8\xb1\xdb\x8c\xd9\x81'), (b'sharif employed', b'\xda\xa9\xd8\xa7\xd8\xb1\xd9\x85\xd9\x86\xd8\xaf \xd8\xb4\xd8\xb1\xdb\x8c\xd9\x81'), (b'other', b'\xd8\xb3\xd8\xa7\xdb\x8c\xd8\xb1')]),
        ),
    ]