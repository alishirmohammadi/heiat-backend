# Generated by Django 2.0.13 on 2020-04-16 19:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pay', '0002_auto_20200416_1857'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='short_address',
            new_name='address',
        ),
    ]