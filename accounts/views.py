from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from userena.decorators import secure_required
from accounts.templatetags.tags import get_tuple
# from  userena.tests.tests_models import UserenaSignupModelTests
from django.core.files.base import ContentFile
# from .forms import ImageUploadForm
from .models import Profile
from django.contrib.auth.decorators import login_required





# Create your views here.
from program.utils import checkMelliCode


def FAQ(request):
    if request.method == 'GET':
        return render(request, 'FAQ.html', {})

def error(request,username=None,page=None):
    if request.method == 'GET':
        return render(request, 'attack.html', {})

def charity(request):
    if request.method == 'GET':
        return render(request, 'Charity.html', {})

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@login_required
def edit(request):
    a = request.user.my_profile
    if request.method == 'GET':

        return render(request, 'profile.html', {'pro': a, 'days': range(1, 32), 'month':get_tuple() ,'allTypes': a.people_type_choices,
                                                 'vazife': a.conscription_choices})
    else:
        a.address = request.POST.get('adress', '')
        a.shenasname = request.POST.get('she_number', '')
        a.people_type = request.POST.get('education', '')
        if (
                    a.people_type == Profile.PEOPLE_TYPE_SHARIF_STUDENT or a.people_type == Profile.PEOPLE_TYPE_SHARIF_GRADUATED or a.people_type == Profile.PEOPLE_TYPE_SHARIF_GRADUATED_NOTSHARIF_STUDENT or a.people_type==Profile.PEOPLE_TYPE_SHARIF_GRADUATED_TALABE):
            k = request.POST.get('student_number', '')
            try:
                val = int(k)
            except ValueError:
                val = None
            a.studentNumber = val
            if (a.studentNumber == None):
                erorr1 = 1
        else:
            a.studentNumber = None

        a.fatherName = request.POST.get('father_name', )
        a.gender = request.POST.get('gender', )
        a.birthYear = request.POST.get('birthyear', )
        a.birthMonth = request.POST.get('birthmonth', )
        a.birthDay = request.POST.get('birthday', )
        a.gender =bool(request.POST.get('gender', ))
        # if (a.gender==True):
        #     a.gender==bool(a.gender)
        # a.gender == bool(a.gender)
        if (request.POST.get('gender', )==True):
            a.conscription = request.POST.get('vazife-type', )
        a.passport = request.POST.get('pas_type', )
        if (request.POST.get('pas_type', ) == 'have'):
            a.passport_number = request.POST.get('serial_pas','' )
            if not(a.passport_number):
                return HttpResponseRedirect('profile.html')
            a.passport_dateofissue = request.POST.get('pas_release','' )
            if not (a.passport_dateofissue):
                return HttpResponseRedirect('profile.html')
            a.passport_dateofexpiry = request.POST.get('pas_exprition','' )
            if not (a.passport_dateofexpiry):
                return HttpResponseRedirect('profile.html')
        if (request.POST.get('coupling', )):
            if (request.POST.get('wife_mellicode', ) != None and checkMelliCode(request.POST.get('wife_mellicode', ))):
                x = request.POST.get('wife_mellicode', )
                datebase_object = Profile.objects.all()
                for type in datebase_object:
                    if (type.melliCode == x):
                        a.couple = type
            else:
                erorr2 = 1
        a.mugshot=request.POST.get('mugshot', )
        a.mugshot=request.FILES.get('mugshot', )
        # a.mugshot.storage = UserenaSignupModelTests.test_upload_mugshot()
        # def upload_pic(request):
        #     if request.method == 'POST':
        # form = ImageUploadForm(request.POST, request.FILES)
        # a.image= form.cleaned_data['image']
                    # return HttpResponse('image upload success')
            # return HttpResponseForbidden('allowed only via POST')
        # a.image=request.POST.get('mugshot',)
        a.mugshot.empty_values=request.POST.get('mugshot-clear', )
        a.save()
        return HttpResponseRedirect('/')



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

                # if success_url:
                #     redirect_to = success_url % {'username': user.username}
                # else:
                #     redirect_to = reverse('userena_profile_detail',
                #                           kwargs={'username': user.username})
                redirect_to='/profile/'
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
