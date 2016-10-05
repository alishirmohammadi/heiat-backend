# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-03 11:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20161003_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='deActivated',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='entranceDate',
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=400, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthDay',
            field=models.IntegerField(null=True, verbose_name='روز تولد'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthMonth',
            field=models.IntegerField(choices=[(1, 'فروردین'), (2, 'اردیبهشت'), (3, 'خرداد'), (4, 'تیر'), (5, 'مرداد'), (6, 'شهریور'), (7, 'مهر'), (8, 'آبان'), (9, 'آذر'), (10, 'دی'), (11, 'بهمن'), (12, 'اسفند')], null=True, verbose_name='ماه تولد'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthYear',
            field=models.IntegerField(default=1370, verbose_name='سال تولد شمسی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cellPhone',
            field=models.CharField(max_length=11, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='conscription',
            field=models.CharField(choices=[('went', 'دارای کارت پایان خدمت'), ('exempt', 'معافیت دایم '), ('educational exempt', 'معافیت تحصیلی'), ('other', 'سایر')], max_length=200, verbose_name='وضعیت نظام وظیفه'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='conscriptionDesc',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='توضیحات بیشتر نظام وظیفه'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='couple',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile', verbose_name='همسر'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='emergencyPhone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره تلفن ضروری'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fatherName',
            field=models.CharField(max_length=200, verbose_name='نام پدر'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.BooleanField(choices=[(True, 'مرد'), (False, 'زن')], default=True, verbose_name='جنسیت'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='passport',
            field=models.CharField(choices=[('have', 'دارم'), ('not have', 'ندارم')], max_length=200, null=True, verbose_name='وضعیت گذرنامه'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='passport_dateofexpiry',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ انقضا گذرنامه به میلادی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='passport_dateofissue',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ صدور گذرنامه به میلادی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='passport_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='شماره گذرنامه'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='people_type',
            field=models.CharField(choices=[('sharif student', 'دانشجو شریف'), ('sharif graduated', 'فارغ التحصیل شریف'), ('sharif graduated talabe', 'فاغ التحصیل شریف و طلبه فعلی'), ('sharif graduated student not sharif', 'فارغ التحصیل شریف و دانشجو سایر'), ('not sharif student', 'دانشجو سایر'), ('not sharif graduated', 'فارغ التحصیل سایر'), ('talabe', 'طلبه'), ('sharif master', 'استاد شریف'), ('sharif employed', 'کارمند شریف'), ('other', 'سایر')], max_length=200, verbose_name='وضعیت تحصیل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='shenasname',
            field=models.CharField(max_length=11, verbose_name='شماره شناسنامه'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='studentNumber',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره دانشجویی'),
        ),
    ]