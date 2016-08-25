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
    entranceDate = models.DateTimeField(max_length=20, default=datetime.now)
    melliCode = models.CharField(max_length=10)
    gender = models.BooleanField(default=1)
    coupling=models.BooleanField(default=1)
    couple = models.ForeignKey('self', null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    shenasname = models.CharField(max_length=11, null=True, blank=True)
    studentNumber = models.CharField(max_length=20, null=True, blank=True)
    fatherName = models.CharField(max_length=200, null=True, blank=True)
    cellPhone = models.CharField(max_length=11)
    emergencyPhone = models.CharField(max_length=20, null=True, blank=True)
    conscriptionDesc = models.CharField(max_length=200, null=True, blank=True)
    deActivated = models.BooleanField(default=False)
    birthYear = models.IntegerField(null=True)
    birthMonth = models.IntegerField(null=True)
    birthDay = models.IntegerField(null=True)
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
    people_type = models.CharField(max_length=200, choices=people_type_choices)
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
    conscription = models.CharField(max_length=200, choices=conscription_choices)

    PASSPORT_NOT_HAVE = 'not have'
    PASSPORT_HAVE = 'have'
    PASSPORT_HAVE_7 = 'have 7'
    passport_choices = (
        (PASSPORT_HAVE, 'دارم'),
        (PASSPORT_HAVE_7, 'دارم ولی کمتر از 7 ماه انقضا دارد '),
        (PASSPORT_NOT_HAVE, 'ندارم'),
    )
    passport = models.CharField(max_length=200, choices=passport_choices, null=True)

    passport_number = models.IntegerField(null=True)
    passport_dateofissue = models.DateField(null=True)

    passport_dateofexpiry = models.DateField(null=True)

    def hasManagement(self):
        from program.models import Management
        manage = Management.objects.filter(profile=self).first()
        return manage
