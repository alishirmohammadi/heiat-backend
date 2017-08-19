"""azzahra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include,patterns
from django.contrib import admin
from accounts.forms import SignupFormExtra, PasswordResetForm
from django.contrib.auth import views as auth_views
from userena.compat import auth_views_compat_quirks, password_reset_uid_kwarg
from userena import settings as userena_settings
from azzahra import settings
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView


def merged_dict(dict_a, dict_b):
    """Merges two dicts and returns output. It's purpose is to ease use of
    ``auth_views_compat_quirks``
    """
    dict_a.update(dict_b)
    return dict_a


urlpatterns = [

    # View profiles
    url(r'^accounts/(?P<username>(?!(signout|signup|signin)/)[\@\.\w-]+)/$',
        'accounts.views.error', ),
    url(r'accounts/^(?P<username>[\@\.\w-]+)/edit/$',
        'accounts.views.error', ),
    url(r'^accounts/page/(?P<page>[0-9]+)/$',
        'accounts.views.error', ),
    url(r'^accounts$',
        'accounts.views.error', ),
    # url(r'^signin/', 'accounts.views.signin'),
    # url(r'^signup/', 'accounts.views.signup'),
    # url(r'^ad/', 'accounts.views.add'),

    url(r'^edit/', 'accounts.views.edit'),
    url(r'^profile/$', 'accounts.views.profile'),
    url(r'^profile/(?P<passport>passport)$', 'accounts.views.profile'),
    url(r'^profile/couple$', 'accounts.views.profile_couple'),
    url(r'^$', RedirectView.as_view(url='/program/'), name='home'),
    # url(r'^accounts/signout/', RedirectView.as_view(url='/accounts/signin', permanent=True), name='home'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', 'accounts.views.activate', name='userena_activate'),
    url(r'^FAQ/$',  TemplateView.as_view(template_name="FAQ.html"), name="FAQ"),
    url(r'^error/', 'accounts.views.error'),


    # url(r'^accounts/edit_profile', 'accounts.views.saveProfile'),

    url(r'^accounts/[\.\w-]+/(mugshots/.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^accounts/[\.\w-]+/edit/(mugshots/.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^admin/', admin.site.urls),
    # url(r'^password_reset/', include('password_reset.urls'), ),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    # url(r'^accounts/password/reset/$','django.contrib.auth.views.password_reset',{'password_reset_form': PasswordResetForm}),
    url(r'^accounts/password/reset/$',
        auth_views.password_reset,
        merged_dict({'template_name': 'userena/password_reset_form.html',
                     'email_template_name': 'userena/emails/password_reset_message.txt',
                     'password_reset_form': PasswordResetForm,
                     'extra_context': {'without_usernames': userena_settings.USERENA_WITHOUT_USERNAMES}
                     }, auth_views_compat_quirks['userena_password_reset']),
        name='userena_password_reset'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^pay/', include('pay.urls')),
    url(r'^program/', include('program.urls')),

]
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += patterns('', (
    r'^static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}
))