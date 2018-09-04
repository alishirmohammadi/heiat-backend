# Encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from accounts.models import Profile
from django.db.models import Sum, Q


# Create your models here.

class Program(models.Model):
    title = models.CharField(max_length=100, default='نام برنامه')
    year = models.IntegerField(null=True, blank=True)
    is_open = models.BooleanField(default=False)
    has_coupling = models.BooleanField(default=False)
    program_interval = models.CharField(default='زمان برنامه', max_length=80)
    register_interval = models.CharField(default='زمان ثبت نام', max_length=80)
    creation_date = models.DateTimeField(auto_now_add=True)
    TYPE_ARBAEEN = 'arbaeen'
    TYPE_ETEKAF = 'etekaf'
    TYPE_MASHHAD = 'mashhad'
    TYPE_MARASEM = 'marasem'
    TYPE_GUEST = 'guest'
    TYPE_SOUTH = 'south'
    TYPE_VOROODI = 'voroodi'

    TYPE_CHOICES = (
        (TYPE_ARBAEEN, 'اربعین'),
        (TYPE_ETEKAF, 'اعتکاف'),
        (TYPE_MASHHAD, 'پابوس عشق'),
        (TYPE_MARASEM, 'مراسم'),
        (TYPE_SOUTH, 'اردو جنوب'),
        (TYPE_VOROODI, 'اردو ورودی ها'),
        (TYPE_GUEST, 'سایر'),

    )
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    base_price = models.IntegerField(null=True, blank=True)
    max_first_installment = models.IntegerField(default=10000000)
    max_second_installment = models.IntegerField(default=10000000)
    STATE_CONFIG = 'config'
    STATE_ACTIVE = 'active'
    STATE_ARCHIVE = 'archive'
    STATE_CHOICES = (
        (STATE_CONFIG, 'در حال پیکربندی'),
        (STATE_ACTIVE, 'فعال'),
        (STATE_ARCHIVE, 'بایگانی'),
    )
    state = models.CharField(max_length=32, choices=STATE_CHOICES, default=STATE_CONFIG)

    class Meta:
        verbose_name = 'برنامه'
        verbose_name_plural = 'برنامه ها'

    def master(self):
        man = Management.objects.filter(role__exact='master manager').filter(program=self).first()
        if man:
            return man.profile
        return '-'

    def sum_of_money(self):
        from pay.models import Payment

        total = Payment.objects.filter(registration__program=self).filter(success=True).aggregate(Sum('amount'))
        return (total['amount__sum'])

    def number_of_register(self):
        total = Registration.objects.filter(program=self).exclude(status__contains=Registration.STATUS_REMOVED).count()
        return total

    def certain_or_came(self):
        total = Registration.objects.filter(program=self).filter(
            Q(status=Registration.STATUS_CERTAIN) | Q(status=Registration.STATUS_CAME)).count()
        return total

    def __str__(self):
        return str(self.title)


class Post(models.Model):
    program = models.ForeignKey(Program, related_name='posts', on_delete=models.CASCADE)
    text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)


class PriceShift(models.Model):
    program = models.ForeignKey(Program, related_name='shifts', on_delete=models.CASCADE)
    people_type = models.CharField(max_length=128, choices=Profile.PEOPLE_TYPE_CHOICES)
    shift = models.IntegerField(default=0)


class Registration(models.Model):
    profile = models.ForeignKey(Profile, related_name='registrations', on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name='registrations', on_delete=models.CASCADE)
    registrationDate = models.DateTimeField(default=datetime.now)
    coupling = models.BooleanField(default=False)
    numberOfPayments = models.IntegerField(default=0)
    STATUS_DEFAULT = 'default'
    STATUS_CERTAIN = 'certain'
    STATUS_RESERVED = 'reserved'
    STATUS_GIVEN_UP = 'given up'
    STATUS_REMOVED = 'removed'
    STATUS_SUSPENDED = 'suspended'
    STATUS_NOT_CHOSEN = 'not chosen'
    STATUS_CAME = 'came'
    STATUS_NOT_CAME = 'not came'
    STATUS_TEMPORARY = 'temporary'
    STATUS_FIRST_STAGE = 'first stage'

    STATUS_CHOICES = (
        (STATUS_DEFAULT, 'منتظر قرعه کشی'),
        (STATUS_CERTAIN, 'قطعی'),
        (STATUS_RESERVED, 'رزرو'),
        (STATUS_GIVEN_UP, 'انصراف'),
        (STATUS_REMOVED, 'پاک شده'),
        (STATUS_SUSPENDED, 'معلق'),
        (STATUS_NOT_CHOSEN, 'انتخاب نشده'),
        (STATUS_CAME, 'شرکت کرده'),
        (STATUS_NOT_CAME, 'شرکت نکرده'),
        (STATUS_TEMPORARY, 'موقت'),
        (STATUS_FIRST_STAGE, 'مرحله اول'),
    )
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=STATUS_DEFAULT)

    class Meta:
        verbose_name = 'ثبت نام'
        verbose_name_plural = 'ثبت نام ها'

    def get_couple_registration(self):
        return Registration.objects.filter(profile=self.profile.couple).filter(program=self.program).filter(
            coupling=True).exclude(status=self.STATUS_REMOVED).first()

    def __str__(self):
        return self.program.title + ' ' + self.profile.user.get_full_name()

    def couple_inconsistency(self):
        if self.program.has_coupling and self.coupling and self.profile.couple:
            coup_reg = self.get_couple_registration()
            if coup_reg and coup_reg.coupling:
                if self.status != coup_reg.status:
                    return True
                elif self.numberOfPayments != coup_reg.numberOfPayments:
                    return True
            else:
                return True
        return False


class Question(models.Model):
    program = models.ForeignKey(Program, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    desc = models.TextField(null=True, blank=True)
    user_sees = models.BooleanField(default=False)
    shift = models.IntegerField(default=0)


class Answer(models.Model):
    registration = models.ForeignKey(Registration, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    yes = models.BooleanField(default=True)


class Management(models.Model):
    program = models.ForeignKey(Program, related_name='managements', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='managements', on_delete=models.CASCADE)
    canEditProgram = models.BooleanField(default=False)
    canFilter = models.BooleanField(default=False)
    canSelect = models.BooleanField(default=False)
    canEditRegistration = models.BooleanField(default=False)
    canMessage = models.BooleanField(default=False)
    canAdd = models.BooleanField(default=False)
    documentation = models.CharField(null=True, blank=True, max_length=10000)
    ROLE_MASTER_MANAGER = 'master manager'
    ROLE_VICAR = 'vicar'
    ROLE_REGISTRATION_MANAGER = 'registration manager'
    ROLE_SISTERS_MANAGER = 'sisters manager'
    ROLE_SISTERS_REGISTRATION_MANAGER = 'sister registration manager'
    ROLE_COMMUNICATION_SISTERS_MANAGER = 'communication sisters manager'
    ROLE_LOGISTIC_MANAGER = 'logistic manager'
    ROLE_LOGISTIC_CREW = 'logistic crew'
    ROLE_EXECUTIVE_MANAGER = 'executive manager'
    ROLE_EXECUTIVE_CREW = 'executive crew'
    ROLE_PANTRY_MANAGER = 'pantry manager'
    ROLE_PANTRY_CREW = 'pantry crew'
    ROLE_ADVERTISING_MANAGER = 'advertising manager'
    ROLE_ADVERTISING_CREW = 'advertising crew'
    ROLE_CREW = 'crew'
    ROLE_KITCHEN_MANAGER = 'kitchen manager'
    ROLE_KITCHEN_VICAR = 'kitchen vicar'
    ROLE_KITCHEN_CREW = 'kitchen crew'
    ROLE_CHOICES = (
        (ROLE_MASTER_MANAGER, 'مسئول برنامه'),
        (ROLE_VICAR, 'جانشین'),
        (ROLE_REGISTRATION_MANAGER, 'مسئول ثبت نام'),
        (ROLE_SISTERS_MANAGER, 'مسئول خواهران'),
        (ROLE_SISTERS_REGISTRATION_MANAGER, 'مسئول ثبت نام خواهران'),
        (ROLE_COMMUNICATION_SISTERS_MANAGER, 'مسئول ارتباط با خواهران'),
        (ROLE_LOGISTIC_MANAGER, 'مسئول تدارکات'),
        (ROLE_LOGISTIC_CREW, 'کادر تداراکات'),
        (ROLE_EXECUTIVE_MANAGER, 'مسئول اجرایی'),
        (ROLE_EXECUTIVE_CREW, 'کادر اجرایی'),
        (ROLE_PANTRY_MANAGER, 'مسئول آبدارخانه'),
        (ROLE_PANTRY_CREW, 'کادر آبدارخانه'),
        (ROLE_ADVERTISING_MANAGER, 'مسئول تبلیغات'),
        (ROLE_ADVERTISING_CREW, 'کادر تبلیغات'),
        (ROLE_CREW, 'کادر'),
        (ROLE_KITCHEN_MANAGER, 'مسئول سلف'),
        (ROLE_KITCHEN_VICAR, 'معاون سلف'),
        (ROLE_KITCHEN_CREW, 'کادر سلف'),
    )
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default=ROLE_MASTER_MANAGER)
    comment = models.CharField(max_length=800, null=True, blank=True)

    class Meta:
        verbose_name = 'مسئولیت'
        verbose_name_plural = 'مسئولیت‌ها'

    def seedocument(self):
        return {
            Management.ROLE_MASTER_MANAGER: [Management.ROLE_MASTER_MANAGER, Management.ROLE_VICAR,
                                             Management.ROLE_REGISTRATION_MANAGER, Management.ROLE_SISTERS_MANAGER,
                                             Management.ROLE_SISTERS_REGISTRATION_MANAGER,
                                             Management.ROLE_COMMUNICATION_SISTERS_MANAGER,
                                             Management.ROLE_LOGISTIC_MANAGER, Management.ROLE_LOGISTIC_CREW,
                                             Management.ROLE_EXECUTIVE_MANAGER,
                                             Management.ROLE_EXECUTIVE_CREW, Management.ROLE_PANTRY_MANAGER,
                                             Management.ROLE_PANTRY_CREW, Management.ROLE_ADVERTISING_MANAGER,
                                             Management.ROLE_ADVERTISING_CREW, Management.ROLE_CREW,
                                             Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_VICAR,
                                             Management.ROLE_KITCHEN_CREW],
            Management.ROLE_VICAR: [Management.ROLE_VICAR, Management.ROLE_REGISTRATION_MANAGER,
                                    Management.ROLE_SISTERS_MANAGER,
                                    Management.ROLE_SISTERS_REGISTRATION_MANAGER,
                                    Management.ROLE_COMMUNICATION_SISTERS_MANAGER,
                                    Management.ROLE_LOGISTIC_MANAGER, Management.ROLE_LOGISTIC_CREW,
                                    Management.ROLE_EXECUTIVE_MANAGER,
                                    Management.ROLE_EXECUTIVE_CREW, Management.ROLE_PANTRY_MANAGER,
                                    Management.ROLE_PANTRY_CREW, Management.ROLE_ADVERTISING_MANAGER,
                                    Management.ROLE_ADVERTISING_CREW, Management.ROLE_CREW,
                                    Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_VICAR,
                                    Management.ROLE_KITCHEN_CREW],
            Management.ROLE_REGISTRATION_MANAGER: [Management.ROLE_REGISTRATION_MANAGER, Management.ROLE_CREW],
            Management.ROLE_SISTERS_MANAGER: [Management.ROLE_SISTERS_MANAGER,
                                              Management.ROLE_SISTERS_REGISTRATION_MANAGER, Management.ROLE_CREW],
            Management.ROLE_COMMUNICATION_SISTERS_MANAGER: [Management.ROLE_COMMUNICATION_SISTERS_MANAGER,
                                                            Management.ROLE_CREW],
            Management.ROLE_LOGISTIC_MANAGER: [Management.ROLE_LOGISTIC_MANAGER, Management.ROLE_CREW,
                                               Management.ROLE_LOGISTIC_CREW, Management.ROLE_PANTRY_MANAGER,
                                               Management.ROLE_PANTRY_CREW,
                                               Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_VICAR,
                                               Management.ROLE_KITCHEN_CREW, Management.ROLE_CREW],
            Management.ROLE_LOGISTIC_CREW: [Management.ROLE_LOGISTIC_CREW, Management.ROLE_CREW],
            Management.ROLE_EXECUTIVE_MANAGER: [Management.ROLE_EXECUTIVE_MANAGER, Management.ROLE_EXECUTIVE_CREW,
                                                Management.ROLE_CREW],
            Management.ROLE_PANTRY_MANAGER: [Management.ROLE_PANTRY_MANAGER, Management.ROLE_CREW,
                                             Management.ROLE_PANTRY_CREW],
            Management.ROLE_PANTRY_CREW: [Management.ROLE_PANTRY_CREW, Management.ROLE_CREW],
            Management.ROLE_ADVERTISING_MANAGER: [Management.ROLE_ADVERTISING_MANAGER, Management.ROLE_CREW,
                                                  Management.ROLE_ADVERTISING_CREW],
            Management.ROLE_ADVERTISING_CREW: [Management.ROLE_ADVERTISING_CREW, Management.ROLE_CREW],
            Management.ROLE_KITCHEN_MANAGER: [Management.ROLE_KITCHEN_MANAGER, Management.ROLE_KITCHEN_CREW,
                                              Management.ROLE_CREW, Management.ROLE_KITCHEN_VICAR],
            Management.ROLE_KITCHEN_VICAR: [Management.ROLE_KITCHEN_VICAR, Management.ROLE_KITCHEN_CREW,
                                            Management.ROLE_CREW],
            Management.ROLE_KITCHEN_CREW: [Management.ROLE_KITCHEN_CREW, Management.ROLE_CREW],
            Management.ROLE_CREW: Management.ROLE_CREW,

        }[self.role]

    def __str__(self):
        return str(self.profile) + '-' + str(self.role) + '-' + str(self.program)


class Message(models.Model):
    registration = models.ForeignKey(Registration, related_name='messages', on_delete=models.CASCADE)
    to_user = models.BooleanField(default=True)
    text = models.TextField()
    send_sms = models.BooleanField(default=False)
    send_date = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return str(self.registration)
