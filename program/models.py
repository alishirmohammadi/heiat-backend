from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce

from accounts.models import Profile

class RegisterState():
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

class Program(models.Model):
    title = models.CharField(max_length=100, default='نام برنامه')
    donate_link = models.CharField(max_length=300, null=True, blank=True)
    donate_text = models.CharField(max_length=300, null=True, blank=True)
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
    base_price = models.IntegerField(default=0)
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
    default_status = models.CharField(max_length=200, choices=RegisterState.STATUS_CHOICES, default=RegisterState.STATUS_DEFAULT)


    class Meta:
        verbose_name = 'برنامه'
        verbose_name_plural = 'برنامه ها'

    def master(self):
        from manage_app.models import Management
        man = self.managements.filter(role=Management.ROLE_MASTER_MANAGER).first()
        if man:
            return man.profile
        return '-'

    def sum_of_money(self):
        from pay.models import Payment

        total = Payment.objects.filter(registration__program=self).filter(success=True).aggregate(Sum('amount'))
        return (total['amount__sum'])

    def number_of_register(self):
        total = Registration.objects.filter(program=self).exclude(status__contains=RegisterState.STATUS_REMOVED).count()
        return total

    def certain_or_came(self):
        total = Registration.objects.filter(program=self).filter(
            Q(status=RegisterState.STATUS_CERTAIN) | Q(status=RegisterState.STATUS_CAME)).count()
        return total

    def users_questions(self):
        return self.questions.filter(user_sees=True)

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
    comment = models.TextField(verbose_name="توضیحات", null=True)
    status = models.CharField(max_length=200, choices=RegisterState.STATUS_CHOICES, default=RegisterState.STATUS_DEFAULT)

    class Meta:
        verbose_name = 'ثبت نام'
        verbose_name_plural = 'ثبت نام ها'

    def get_couple_registration(self):
        return Registration.objects.filter(profile=self.profile.couple).filter(program=self.program).filter(
            coupling=True).exclude(status=RegisterState.STATUS_REMOVED).first()

    def couple_id(self):
        reg=self.get_couple_registration()
        if reg:
            return reg.id
        return None
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

    def sum_payed(self):
        return self.payments.filter(success=True).aggregate(sum_amount=Coalesce(Sum('amount'), 0)).get('sum_amount', 0)

    def nominal_price(self):
        ans = self.program.base_price
        shift = self.program.shifts.filter(people_type=self.profile.people_type).first()
        if shift:
            ans = ans + shift.shift
        for answer in self.answers.all():
            if answer.question.var == Question.VAR_MULTIPLE:
                if answer.answer_text and answer.question.shift != '':
                    s = answer.question.shift.split('-')
                    ans += int(s[int(answer.answer_text)])
            if answer.question.var == Question.VAR_YESNO:
                if answer.yes and answer.question.shift != '':
                    ans += int(answer.question.shift)
        return ans

    def next_installment(self):
        res = self.nominal_price() - self.sum_payed()
        if self.numberOfPayments == 0:
            return min(res, self.program.max_first_installment)
        if self.numberOfPayments == 1:
            return min(res, self.program.max_second_installment)
        return res

    def last_from_user_message(self):
        return self.messages.filter(to_user=False).order_by('-id').first()


class Question(models.Model):
    program = models.ForeignKey(Program, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    desc = models.TextField(null=True, blank=True)
    params = models.TextField(null=True, blank=True)
    user_sees = models.BooleanField(default=False)
    shift = models.TextField()
    VAR_YESNO = 'yesno'
    VAR_MULTIPLE = 'multiple'
    VAR_FILE = 'file'
    VAR_CHOICES = (
        (VAR_YESNO, 'بله خیر'),
        (VAR_MULTIPLE, 'چند گزینه ای'),
        (VAR_FILE, 'فایل'),
    )
    var = models.CharField(max_length=20, choices=VAR_CHOICES, default=VAR_YESNO)

    def __str__(self):
        return self.title


class Answer(models.Model):
    registration = models.ForeignKey(Registration, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    yes = models.BooleanField(default=True)
    answer_text = models.TextField(null=True, blank=True)
    answer_file = models.FileField(upload_to ='uploads/', null=True, blank=True) 
    def __str__(self):
        return self.question.title + '-' + self.registration.profile.user.get_full_name()


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

#
# @receiver(post_save, sender=Message)
# def sens_sms(sender, instance=None, created=False, **kwargs):
#     if created and not kwargs.get('raw', False):
#         if instance.to_user and instance.send_sms:
#             Profile.objects.create(user=instance)
