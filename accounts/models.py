# Encoding: utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    PEOPLE_TYPE_SHARIF_STUDENT = 'sharif student'
    PEOPLE_TYPE_SHARIF_GRADUATED = 'sharif graduated'
    PEOPLE_TYPE_SHARIF_GRADUATED_TALABE = 'sharif graduated talabe'
    PEOPLE_TYPE_SHARIF_GRADUATED_NOTSHARIF_STUDENT = 'sharif graduated student not sharif'
    PEOPLE_TYPE_NOTSHARIF_STUDENT = 'not sharif student'
    PEOPLE_TYPE_NOTSHARIF_GRADUATED = 'not sharif graduated'
    PEOPLE_TYPE_TALABE = 'talabe'
    PEOPLE_TYPE_SHARIF_MASTER = 'sharif master'
    PEOPLE_TYPE_SHARIF_EMPLOYED = 'sharif employed'
    PEOPLE_TYPE_OTHER = 'other'
    PEOPLE_TYPE_CHOICES = (
        (PEOPLE_TYPE_SHARIF_STUDENT, 'دانشجو شریف'),
        (PEOPLE_TYPE_SHARIF_GRADUATED, 'فارغ التحصیل شریف'),
        (PEOPLE_TYPE_SHARIF_GRADUATED_TALABE, 'فاغ التحصیل شریف و طلبه فعلی'),
        (PEOPLE_TYPE_SHARIF_GRADUATED_NOTSHARIF_STUDENT, 'فارغ التحصیل شریف و دانشجو سایر'),
        (PEOPLE_TYPE_NOTSHARIF_STUDENT, 'دانشجو سایر'),
        (PEOPLE_TYPE_NOTSHARIF_GRADUATED, 'فارغ التحصیل سایر'),
        (PEOPLE_TYPE_TALABE, 'طلبه'),
        (PEOPLE_TYPE_SHARIF_MASTER, 'استاد شریف'),
        (PEOPLE_TYPE_SHARIF_EMPLOYED, 'کارمند شریف'),
        (PEOPLE_TYPE_OTHER, 'سایر'),
    )
    people_type = models.CharField(max_length=200, choices=PEOPLE_TYPE_CHOICES, default=PEOPLE_TYPE_OTHER,
                                   verbose_name='وضعیت تحصیل')
    student_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="شماره دانشجویی")
    GENDER_CHOICES = ((True, 'مرد'), (False, 'زن'))
    gender = models.BooleanField(default=True, choices=GENDER_CHOICES, verbose_name="جنسیت")
    couple = models.ForeignKey('self', null=True, verbose_name="همسر", blank=True)
    father_name = models.CharField(max_length=200, verbose_name="نام پدر", null=True)
    mobile = models.CharField(max_length=11, verbose_name="شماره موبایل", null=True)
    PASSPORT_NOT_HAVE = 'not have'
    PASSPORT_HAVE = 'have'
    PASSPORT_CHOICES = (
        (PASSPORT_HAVE, 'دارم'),
        (PASSPORT_NOT_HAVE, 'ندارم'),
    )
    passport = models.CharField(max_length=200, choices=PASSPORT_CHOICES, null=True, verbose_name="وضعیت گذرنامه")
    passport_number = models.CharField(null=True, blank=True, verbose_name="شماره گذرنامه", max_length=10)
    passport_date_of_issue = models.DateField(null=True, blank=True, verbose_name="تاریخ صدور گذرنامه به میلادی")
    passport_date_of_expiry = models.DateField(null=True, blank=True, verbose_name="تاریخ انقضا گذرنامه به میلادی")
    CONSCRIPTION_WENT = 'went'
    CONSCRIPTION_EXEMPT = 'exempt'
    CONSCRIPTION_EDUCATIONAL_EXEMPT = 'educational exempt'
    CONSCRIPTION_ARMY = 'army'
    CONSCRIPTION_RESPITE = 'respite'
    CONSCRIPTION_WITHOUT_CONDITION = 'without_condition'
    CONSCRIPTION_OTHER = 'other'
    conscription_choices = (
        (CONSCRIPTION_WENT, 'دارای کارت پایان خدمت'),
        (CONSCRIPTION_EXEMPT, 'معافیت دایم '),
        (CONSCRIPTION_EDUCATIONAL_EXEMPT, 'معافیت تحصیلی'),
        (CONSCRIPTION_ARMY, 'نظامی'),
        (CONSCRIPTION_WITHOUT_CONDITION, 'غیر مشمول'),
        (CONSCRIPTION_RESPITE, 'مهلت قانونی معرفی'),
        (CONSCRIPTION_OTHER, 'سایر'),
    )
    conscription = models.CharField(max_length=200, choices=conscription_choices, verbose_name="وضعیت نظام وظیفه")
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حسابهای کاربری'
