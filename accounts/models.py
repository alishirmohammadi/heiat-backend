# Encoding: utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
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
    people_type_choices = (
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
    people_type = models.CharField(max_length=200, choices=people_type_choices,default=PEOPLE_TYPE_OTHER,verbose_name='وضعیت تحصیل')
    studentNumber = models.CharField(max_length=20, null=True,blank=True,verbose_name="شماره دانشجویی")
    GENDER_CHOICES = ((True, 'مرد'), (False, 'زن'))
    gender = models.BooleanField(default=True,choices=GENDER_CHOICES,verbose_name="جنسیت")
    couple = models.ForeignKey('self', null=True,verbose_name="همسر")
    address = models.CharField(max_length=400,verbose_name="آدرس",null=True)
    shenasname = models.CharField(max_length=11,verbose_name="شماره شناسنامه",null=True)
    fatherName = models.CharField(max_length=200,verbose_name="نام پدر",null=True)
    cellPhone = models.CharField(max_length=11,verbose_name="شماره موبایل",null=True)
    emergencyPhone = models.CharField(max_length=20, null=True,verbose_name="شماره تلفن ضروری")
    # deActivated = models.BooleanField(default=False,verbose_name="")
    birthYear = models.IntegerField(default=1370,verbose_name="سال تولد شمسی")
    MONTH_CHOICES = (
    (1, 'فروردین'), (2, 'اردیبهشت'), (3, 'خرداد'), (4, 'تیر'), (5, 'مرداد'), (6, 'شهریور'), (7, 'مهر'), (8, 'آبان'),
    (9, 'آذر'),
    (10, 'دی'), (11, 'بهمن'), (12, 'اسفند'))
    birthMonth = models.IntegerField(null=True,choices=MONTH_CHOICES,verbose_name="ماه تولد")
    birthDay = models.IntegerField(null=True,verbose_name="روز تولد")


    PASSPORT_NOT_HAVE = 'not have'
    PASSPORT_HAVE = 'have'
    passport_choices = (
        (PASSPORT_HAVE, 'دارم'),
        (PASSPORT_NOT_HAVE, 'ندارم'),
    )
    passport = models.CharField(max_length=200, choices=passport_choices, null=True,verbose_name="وضعیت گذرنامه")
    passport_number = models.IntegerField(null=True, blank=True,verbose_name="شماره گذرنامه")
    passport_dateofissue = models.DateField(null=True, blank=True,verbose_name="تاریخ صدور گذرنامه به میلادی")
    passport_dateofexpiry = models.DateField(null=True, blank=True,verbose_name="تاریخ انقضا گذرنامه به میلادی")
    CONSCRIPTION_WENT = 'went'
    CONSCRIPTION_EXEMPT = 'exempt'
    CONSCRIPTION_EDUCATIONAL_EXEMPT = 'educational exempt'
    CONSCRIPTION_OTHER = 'other'
    conscription_choices = (
        (CONSCRIPTION_WENT, 'دارای کارت پایان خدمت'),
        (CONSCRIPTION_EXEMPT, 'معافیت دایم '),
        (CONSCRIPTION_EDUCATIONAL_EXEMPT, 'معافیت تحصیلی'),
        (CONSCRIPTION_OTHER, 'سایر'),
    )
    conscription = models.CharField(max_length=200, choices=conscription_choices,verbose_name="وضعیت نظام وظیفه")
    conscriptionDesc = models.CharField(max_length=200, null=True, blank=True,verbose_name="توضیحات بیشتر نظام وظیفه")

    def hasManagement(self):
        from program.models import Management

        manage = Management.objects.filter(profile=self).first()
        return manage

    def coupling(self):
        if self.couple == None:
            return False
        return True

    def registered_on_last(self):
        from program.models import Registration
        from program.utils import getLastProgram

        return Registration.objects.filter(profile=self).filter(program=getLastProgram()).exclude(
            status=Registration.STATUS_REMOVED).first()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حسابهای کاربری'
