from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from userena.decorators import secure_required
from guardian.decorators import permission_required_or_403


# Create your views here.
def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def farsiNumber(Num):
    Num1 = str(Num)
    Num1.replace('1', '1')
    Num1.replace('1', '2')
    Num1.replace('1', '3')
    Num1.replace('1', '4')
    Num1.replace('1', '5')
    Num1.replace('1', '6')
    Num1.replace('1', '7')
    Num1.replace('1', '8')
    Num1.replace('1', '9')


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
            return False
    else:
        return False


def signin(request, post_id):
    if post_id == '1':
        return render(request, 'signin.html', {'message_id': post_id})
    else:
        if request.method == 'GET':
            return render(request, 'signin.html', {})
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:

                print("User is valid, active and authenticated")
                login(request, user)
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
        return HttpResponseRedirect('/')


def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {})
    else:
        password1 = request.POST.get('password', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')

        cellphone = request.POST.get('cellphone', '')
        mellicode = request.POST.get('mellicode', '')
        error = False
        if User.objects.filter(username__exact=mellicode):
            error = True
            return render(request, 'signup.html', {'error3': error,
                                                   'first_name': firstname,
                                                   'last_name': lastname,
                                                   'email': email,
                                                   'mellicode': mellicode,
                                                   'cellphone': cellphone})
        if validateEmail(email) == False:
            error = True
            return render(request, 'signup.html', {'error2': error,
                                                   'first_name': firstname,
                                                   'last_name': lastname,
                                                   'email': email,
                                                   'mellicode': mellicode,
                                                   'cellphone': cellphone})
        if checkMelliCode(mellicode) == False:
            error = True
            return render(request, 'signup.html', {'error1': error,
                                                   'first_name': firstname,
                                                   'last_name': lastname,
                                                   'email': email,
                                                   'mellicode': mellicode,
                                                   'cellphone': cellphone})

        user1 = User.objects.create_user(username=mellicode,
                                         email=email,
                                         password=password1,
                                         first_name=firstname,
                                         last_name=lastname)
        user1.is_active = False
        user1.save()
        profile1 = Profile()
        profile1.cellPhone = cellphone
        profile1.melliCode = mellicode
        profile1.user = user1
        profile1.save()
        return HttpResponseRedirect('/1')




def FAQ(request):
    if request.method == 'GET':
        return render(request, 'FAQ.html', {'allTypes': Profile.people_type_choices})

def charity(request):
        if request.method == 'GET':
            return render(request, 'Charity.html', {'allTypes': Profile.people_type_choices})


#
def edit(request):
    a = request.user.my_profile
    if request.method == 'GET':

        return render(request, 'profile.html', {'pro': a, 'days': range(1, 32), 'allTypes': a.people_type_choices,
                                                'pas_type': a.passport_choices, 'vazife': a.conscription_choices})
    else:
        a.address = request.POST.get('adress', )
        a.shenasname = request.POST.get('she_number', )
        a.people_type = request.POST.get('education', )
        # if(a.my_profile.people_type =! 'sharif student' and a.my_profile.people_type == 'sharif graduated' and a.my_profile.people_type =! 'sharif graduated talabe'):
        t = (request.POST.get('student_number'))
        a.studentNumber = t
        a.fatherName = request.POST.get('father_name', )
        a.gender = request.POST.get('gender', )
        # a.conscription=request.POST.get('vazife_type')
        # a.passport=request.POST.get('pas_type',)
        # a.passport_serial=request.POST.get('serial_pas',)
        # a.passport_release=request.POST.get('pas_release',)
        # a.passport_exprition=request.POST.get('pas_exprition',)
        # a.couple=request.POST.get('coupling')

        a.save()
        return HttpResponseRedirect('/')


def manage_nav(request):
    if request.user.is_anonymous:
        manage = False
        return render(request, 'base.html', {'manage': manage})
    else:
        a = request.user.my_profile
        from program.models import Management
        manage = Management.objects.filter(profile=a).first()

        if request.method == 'GET':
            return render(request, 'base.html', {'profile': a, 'manage': manage})

@secure_required
def activate(request, activation_key,
             template_name='userena/activate_fail.html',
             retry_template_name='userena/activate_retry.html',
             success_url=None, extra_context=None):
    """
    Activate a user with an activation key.

    The key is a SHA1 string. When the SHA1 is found with an
    :class:`UserenaSignup`, the :class:`User` of that account will be
    activated.  After a successful activation the view will redirect to
    ``success_url``.  If the SHA1 is not found, the user will be shown the
    ``template_name`` template displaying a fail message.
    If the SHA1 is found but expired, ``retry_template_name`` is used instead,
    so the user can proceed to :func:`activate_retry` to get a new activation key.

    :param activation_key:
        String of a SHA1 string of 40 characters long. A SHA1 is always 160bit
        long, with 4 bits per character this makes it --160/4-- 40 characters
        long.

    :param template_name:
        String containing the template name that is used when the
        ``activation_key`` is invalid and the activation fails. Defaults to
        ``userena/activate_fail.html``.

    :param retry_template_name:
        String containing the template name that is used when the
        ``activation_key`` is expired. Defaults to
        ``userena/activate_retry.html``.

    :param success_url:
        String containing the URL where the user should be redirected to after
        a successful activation. Will replace ``%(username)s`` with string
        formatting if supplied. If ``success_url`` is left empty, will direct
        to ``userena_profile_detail`` view.

    :param extra_context:
        Dictionary containing variables which could be added to the template
        context. Default to an empty dictionary.

    """
    from userena.models import UserenaSignup
    from userena import settings as userena_settings
    from django.contrib import messages
    from django.core.urlresolvers import reverse
    from django.shortcuts import redirect
    from userena.views import ExtraContextTemplateView
    from django.utils.translation import ugettext as _

    try:
        if (not UserenaSignup.objects.check_expired_activation(activation_key)
            or not userena_settings.USERENA_ACTIVATION_RETRY):
            user = UserenaSignup.objects.activate_user(activation_key)
            if user:
                # Sign the user in.
                auth_user = authenticate(identification=user.username,
                                         check_password=False)
                login(request, auth_user)

                if userena_settings.USERENA_USE_MESSAGES:
                    messages.success(request, _('Your account has been activated and you have been signed in.'),
                                     fail_silently=True)

                if success_url: redirect_to = success_url % {'username': user.username }
                else: redirect_to = reverse('userena_profile_detail',
                                            kwargs={'username': user.username})
                return redirect(redirect_to)
            else:
                if not extra_context: extra_context = dict()
                return ExtraContextTemplateView.as_view(template_name=template_name,
                                                        extra_context=extra_context)(
                                        request)
        else:
            if not extra_context: extra_context = dict()
            extra_context['activation_key'] = activation_key
            return ExtraContextTemplateView.as_view(template_name=retry_template_name,
                                                extra_context=extra_context)(request)
    except UserenaSignup.DoesNotExist:
        if not extra_context: extra_context = dict()
        return ExtraContextTemplateView.as_view(template_name=template_name,
                                                extra_context=extra_context)(request)
