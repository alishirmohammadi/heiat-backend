# Generated by Django 2.0.13 on 2021-01-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0007_auto_20210130_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='shift',
            field=models.TextField(),
        ),
    ]
