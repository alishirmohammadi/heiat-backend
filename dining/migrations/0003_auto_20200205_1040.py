# Generated by Django 2.0.13 on 2020-02-05 10:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dining', '0002_auto_20200205_0623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodreception',
            old_name='type',
            new_name='status',
        ),
    ]