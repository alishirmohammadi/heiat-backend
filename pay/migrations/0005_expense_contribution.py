# Generated by Django 2.0.13 on 2020-04-25 22:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('pay', '0004_expense_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='contribution',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
