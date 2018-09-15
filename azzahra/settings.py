from django.conf import settings
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!%k2v4k!9*(%@ft_by9gh02%#n@b^vfiljin^3h+n!9&qj7_ds'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'accounts',
    'program',
    'pay',

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
        'accounts.throttles.BurstUserRateThrottle',
        'accounts.throttles.SustainedUserRateThrottle',
        'accounts.throttles.BurstAnonRateThrottle',
        'accounts.throttles.SustainedAnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'burst_user': '90/min',
        'burst_anon': '30/min',
        'sustained_user': '3000/day',
        'sustained_anon': '1000/day',
    }
}

DJOSER = {
    # 'DOMAIN': local.FRONT_DOMAIN_LOCAL,
    # 'SITE_NAME': 'جمع‌نویسی',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_VALIDATORS': [],
    'SERIALIZERS': {
        'user': 'accounts.serializers.UserSerializer',
        'user_create': 'accounts.serializers.UserRegisterSerializer'
    },
}

ROOT_URLCONF = 'azzahra.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'azzahra.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'baharloo.omid'
EMAIL_HOST_PASSWORD = 'yakarim2'
DEFAULT_FROM_EMAIL = 'هیئت الزهرا<baharloo.omid@gmail.com>'
SERVER_EMAIL = EMAIL_HOST_USER
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

from django.utils.translation import ugettext_lazy as _


LANGUAGES = (
    ('fa', _('Farsi')),
    # ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

ADMINS = (('Omid Baharloo', 'omid.gonbad@gmail.com'),)
from .local import *

STATIC_ROOT = STATIC_ROOT_LOCAL
STATIC_URL = '/static/'
MEDIA_ROOT = MEDIA_ROOT_LOCAL
MEDIA_URL = '/media/'
DATABASES = DATABASES_LOCAL
SITE_ID = 1
CORS_ORIGIN_ALLOW_ALL = True
