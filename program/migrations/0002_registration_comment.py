# Generated by Django 2.0.13 on 2020-02-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='comment',
            field=models.TextField(null=True, verbose_name='توضیحات'),
        ),
    ]