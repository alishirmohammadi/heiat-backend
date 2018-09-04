# Generated by Django 2.0.8 on 2018-09-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20180904_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='conscription',
            field=models.CharField(blank=True, choices=[('went', 'دارای کارت پایان خدمت'), ('exempt', 'معافیت دایم '), ('educational exempt', 'معافیت تحصیلی'), ('army', 'نظامی'), ('without_condition', 'غیر مشمول'), ('respite', 'مهلت قانونی معرفی'), ('other', 'سایر')], max_length=200, null=True, verbose_name='وضعیت نظام وظیفه'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='father_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='نام پدر'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='passport',
            field=models.CharField(blank=True, choices=[('have', 'دارم'), ('not have', 'ندارم')], max_length=200, null=True, verbose_name='وضعیت گذرنامه'),
        ),
    ]
