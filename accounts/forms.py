# encoding:utf-8
from __future__ import unicode_literals

from userena.forms import (SignupForm, SignupFormOnlyEmail, AuthenticationForm,
                           ChangeEmailForm, EditProfileForm)

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from userena import settings as userena_settings
from userena.models import UserenaSignup
from userena.utils import get_profile_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

attrs_dict = {'class': 'required'}
USERNAME_RE = r'^[\.\w]+$'
from hashlib import sha1
import random
from django import forms


class SignupFormExtra(SignupForm):
    """
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.


    """
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("کدملی "),
                                error_messages={
                                    'invalid': _('این قسمت فقط مخصوص کد ملی می باشد')})

    first_name = forms.CharField(label=_(u'نام '),
                                 max_length=30,
                                 required=False)

    last_name = forms.CharField(label=_(u'نام خانوادگی '),
                                max_length=30,
                                required=False)
    cellPhone = forms.CharField(label=_(u'تلفن همراه '),
                                max_length=30,
                                required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("ایمیل "))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("رمز عبور "))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("تکرار رمز "))

    def __init__(self, *args, **kw):
        """

        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        # new_order = self.fields.keyOrder[:-2]
        # new_order.insert(0, 'first_name')
        # new_order.insert(1, 'last_name')
        # self.fields.keyOrder = new_order

    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        username, email, password = (self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'])

        new_user = UserenaSignup.objects.create_user(username,
                                                     email,
                                                     password,
                                                     not userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                     False)

        # Get the profile, the `save` method above creates a profile for each
        # user because it calls the manager method `create_user`.
        # See: https://github.com/bread-and-pepper/django-userena/blob/master/userena/managers.py#L65
        # user_profile = new_user.get_profile()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        p = new_user.my_profile
        p.cellPhone = self.cleaned_data['cellPhone']
        p.melliCode = self.cleaned_data['username']
        p.save()
        new_user.userena_signup.send_activation_email()
        return new_user
        # Userena expects to get the new user from this form, so return the new
        # user.

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.
        Also validates that the username is not listed in
        ``USERENA_FORBIDDEN_USERNAMES`` list.
        """
        try:
            user = get_user_model().objects.get(username__iexact=self.cleaned_data['username'])
        except get_user_model().DoesNotExist:
            if checkMelliCode(self.cleaned_data['username']):
                pass
        else:
            if userena_settings.USERENA_ACTIVATION_REQUIRED and UserenaSignup.objects.filter(
                    user__username__iexact=self.cleaned_data['username']).exclude(
                activation_key=userena_settings.USERENA_ACTIVATED):
                raise forms.ValidationError(_(
                    'این کدملی پیش تر در سیستم ثبت شده ولی فعال نشده است. لطفا برای فعال سازی ایمیل خود را چک نمایید'))
            raise forms.ValidationError(_('این کدملی پیش تر ثبت شده است'))
        if self.cleaned_data['username'].lower() in userena_settings.USERENA_FORBIDDEN_USERNAMES:
            raise forms.ValidationError(_('این کدملی مجاز نمی باشد'))
        return self.cleaned_data['username']

    def clean_email(self):
        """ Validate that the e-mail address is unique. """
        if get_user_model().objects.filter(email__iexact=self.cleaned_data['email']):
            if userena_settings.USERENA_ACTIVATION_REQUIRED and UserenaSignup.objects.filter(
                    user__email__iexact=self.cleaned_data['email']).exclude(
                activation_key=userena_settings.USERENA_ACTIVATED):
                raise forms.ValidationError(_(
                    'این ایمیل پیش تر در سیستم ثبت شده ولی فعال نگردیده است. لطفا ایمیل خود را برای فعال سازی چک نمایید'))
        return self.cleaned_data['email']

    def clean_cellPhone(self):
        if checkCellPhone(self.cleaned_data['cellPhone']):
            return self.cleaned_data['cellPhone']

    def clean(self):
        """
        Validates that the values entered into the two password fields match.
        Note that an error here will end up in ``non_field_errors()`` because
        it doesn't apply to a single field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("گذرواژه های وارد شده یکسان نیستند"))
        return self.cleaned_data
        #
        # def save(self):
        #     """ Creates a new user and account. Returns the newly created user. """
        #
        #     username, email, password = (self.cleaned_data['username'],
        #                                  self.cleaned_data['email'],
        #                                  self.cleaned_data['password1'])
        #
        #     new_user = UserenaSignup.objects.create_user(username,
        #                                                  email,
        #                                                  password,
        #                                                  not userena_settings.USERENA_ACTIVATION_REQUIRED,
        #                                                  userena_settings.USERENA_ACTIVATION_REQUIRED)
        #     return new_user


from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['people_type', 'studentNumber', 'gender', 'address', 'shenasname',
                  'fatherName', 'emergencyPhone', 'birthYear', 'birthMonth', 'birthDay']
        widgets = {
            'gender': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.fields['gender'].widget = forms.RadioSelect

    def clean(self):
        cleaned_data=self.cleaned_data
        if cleaned_data.get('people_type') not in [Profile.PEOPLE_TYPE_SHARIF_STUDENT,Profile.PEOPLE_TYPE_SHARIF_GRADUATED_NOTSHARIF_STUDENT,Profile.PEOPLE_TYPE_SHARIF_GRADUATED_TALABE,Profile.PEOPLE_TYPE_SHARIF_GRADUATED]:
            if 'studentNumber' in self.errors:
                del self.errors['studentNumber']
                cleaned_data['studentNumber']=None
        return cleaned_data

    def clean_birthDay(self):
        day = self.cleaned_data['birthDay']
        if not day or day < 1 or day > 31:
            raise forms.ValidationError('روز تولد معتبر نیست')
        return day

    def clean_studentNumber(self):
        stu=self.cleaned_data['studentNumber']
        if not stu:
            raise forms.ValidationError(_('شماره دانشجویی نمی تواند خالی باشد'))
        other=Profile.objects.filter(studentNumber=stu).first()
        from .views import isNum
        if not isNum(stu) or len(stu)!=8:
            raise forms.ValidationError(_('فرمت شماره دانشجویی درست نیست'))
        if other and other.id != self.instance.id:
            raise forms.ValidationError(_('شماره دانشجویی تکراری است'))
        return stu

class ProfilePassportForm(forms.ModelForm):
    # error_css_class = 'error'
    class Meta:
        model = Profile
        # exclude = ['privacy', 'user', 'entranceDate', 'deActivated', 'couple', 'cellPhone', 'gender', 'address', 'shenasname',
        #            'studentNumber', 'fatherName', 'emergencyPhone', 'birthYear', 'birthMonth', 'birthDay',
        #            'people_type']
        fields = ['conscription',
                  'conscriptionDesc', 'passport', 'passport_number', 'passport_dateofissue', 'passport_dateofexpiry',
                  'mugshot']
        widgets = {
            'passport_dateofissue': forms.DateInput(attrs={'class': 'datepicker'}),
            'passport_dateofexpiry': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        labels = {
            'mugshot': 'عکس گذرنامه'
        }
        help_texts = {
            'mugshot': "عکس ۲ در ۳ مشابه عکس گذرنامه برای مانیفست",
            "passport_number": "به صورت ۸ رقمی و بدون حرف اول"

        }

    def __init__(self, *args, **kwargs):
        super(ProfilePassportForm, self).__init__(*args, **kwargs)


class PasswordResetForm(forms.Form):
    username = forms.CharField(label=_("کدملی"), max_length=60)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, username):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = get_user_model()._default_manager.filter(
            username__iexact=username, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        username = self.cleaned_data["username"]
        for user in self.get_users(username):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)


def checkMelliCode(mellicode):
    a = mellicode
    if (len(a) == 8):
        a = '00' + a
    if (len(a) == 9):
        a = '0' + a
    print(a)
    if (len(a) == 10):
        r = 0
        for i in range(0, 9):
            r1 = int(a[i]) * (10 - i)
            r = r1 + r
        c = r % 11
        if (int(a[9]) == 1) and (c == 1):
            return True
        elif (int(a[9]) == 0) and (c == 0):
            return True
        elif (int(a[9]) == 11 - c):
            return True
        else:
            raise forms.ValidationError(_('کد ملی وارد شده معتبر نیست'))
    else:
        raise forms.ValidationError(_('کد ملی وارد شده معتبر نیست'))


def checkCellPhone(cellPhone):
    a = cellPhone
    if (len(a) == 10 and int(a[0]) == 9):
        a = '0' + a
    if (len(a) == 11):
        if (int(a[0]) == 0 and int(a[1]) == 9):
            return True
        else:
            raise forms.ValidationError(_('شماره تلفن وارد شده متعلق به ایران نمی باشد'))
    else:
        raise forms.ValidationError(_('شماره تلفن وارد شده صحیح نمی باشد'))
