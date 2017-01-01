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
    isOpen = models.BooleanField(default=False)
    additionalOption = models.CharField(max_length=30, null=True, blank=True)
    hasCoupling = models.BooleanField(default=False)
    isPublic = models.BooleanField(default=False)
    programInterval = models.CharField(default='زمان برنامه', max_length=80)
    registerInterval = models.CharField(default='زمان ثبت نام', max_length=80)
    creationDate = models.DateTimeField(default=datetime.now)
    notes = models.CharField(max_length=20000)
    email = models.EmailField(max_length=200, null=True, blank=True)
    emailPassword = models.CharField(max_length=200, null=True, blank=True)
    startDate = models.DateField(default=date.today)
    TYPE_ARBAEEN = 'arbaeen'
    TYPE_ETEKAF = 'etekaf'
    TYPE_MASHHAD = 'mashhad'
    TYPE_MARASEM = 'marasem'
    type_choices = (
        (TYPE_ARBAEEN, 'اربعین'),
        (TYPE_ETEKAF, 'اعتکاف'),
        (TYPE_MASHHAD, 'پابوس عشق'),
        (TYPE_MARASEM, 'مراسم'),

    )
    type = models.CharField(max_length=200, choices=type_choices)

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

    def pricings(self):
        return Pricing.objects.filter(program=self)


class Registration(models.Model):
    profile = models.ForeignKey(Profile)
    program = models.ForeignKey(Program)
    registrationDate = models.DateTimeField(default=datetime.now)
    additionalOption = models.BooleanField(default=False)
    label1 = models.BooleanField(default=False)
    label2 = models.BooleanField(default=False)
    label3 = models.IntegerField(default=0)
    label4 = models.IntegerField(default=0)
    coupling = models.BooleanField(default=False)
    feedBack = models.CharField(max_length=2000, null=True, blank=True)
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

    status_choices = (
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
    status = models.CharField(max_length=200, choices=status_choices, default=STATUS_DEFAULT)

    class Meta:
        verbose_name = 'ثبت نام'
        verbose_name_plural = 'ثبت نام ها'

    def get_couple_registration(self):
        return Registration.objects.filter(profile=self.profile.couple).filter(program=self.program).filter(coupling=True).exclude(status=self.STATUS_REMOVED).first()

    def get_pricing(self):
        pr1 = Pricing.objects.filter(program=self.program).filter(people_type=self.profile.people_type).filter(
            coupling=self.coupling).filter(
            additionalOption=self.additionalOption).first()
        if not pr1 and self.get_couple_registration:
            return self.get_couple_registration().get_pricing()
        return pr1

    def get_num_of_installments(self):
        p = self.get_pricing()
        if p.price3:
            return 3
        if p.price2:
            return 2
        if p.price1:
            return 1
        return 0

    def __str__(self):
        return self.program.title + ' ' + self.profile.user.get_full_name()

    def couple_inconsistency(self):
        if self.program.hasCoupling and self.coupling and self.profile.couple:
            coup_reg =self.get_couple_registration()
            if coup_reg and coup_reg.coupling:
                if self.status != coup_reg.status:
                    return True
                elif self.numberOfPayments != coup_reg.numberOfPayments:
                    return True
            else:
                return True
        return False


class Management(models.Model):
    program = models.ForeignKey(Program)
    profile = models.ForeignKey(Profile)
    canEditProgram = models.BooleanField(default=False)
    canFilter = models.BooleanField(default=False)
    canSelect = models.BooleanField(default=False)
    canEditRegistration = models.BooleanField(default=False)
    canDocument = models.BooleanField(default=False)
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
    role_choices = (
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
    role = models.CharField(max_length=200, choices=role_choices, default=ROLE_MASTER_MANAGER)
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


class Pricing(models.Model):
    program = models.ForeignKey(Program)
    price1 = models.IntegerField(null=True, blank=True)
    price2 = models.IntegerField(null=True, blank=True)
    price3 = models.IntegerField(null=True, blank=True)
    coupling = models.BooleanField(default=False)
    additionalOption = models.BooleanField(default=False)
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

    def __str__(self):
        return self.people_type + ' ' + ' ' + self.program.title

    class Meta:
        verbose_name = 'قیمت'
        verbose_name_plural = 'قیمت ها'


class Message(models.Model):
    sender = models.ForeignKey(Management)
    subject = models.CharField(max_length=200, null=True, blank=True)
    content = models.CharField(max_length=1000, null=True, blank=True)
    sendEmail = models.BooleanField(default=False)
    sendSms = models.BooleanField(default=False)
    sendInbox = models.BooleanField(default=False)
    messageSendDate = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return str(self.sender)


class Message_reciving(models.Model):
    message = models.ForeignKey(Message)
    registration = models.ForeignKey(Registration)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'دریافت پیام'
        verbose_name_plural = 'دریافت پیام ها'
