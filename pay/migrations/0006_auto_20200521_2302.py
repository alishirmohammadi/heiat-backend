# Generated by Django 2.0.13 on 2020-05-21 23:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('pay', '0005_expense_contribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='boolean_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]