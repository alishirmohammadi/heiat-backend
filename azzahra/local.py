import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES_LOCAL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'HOST':'213.233.161.70',
        'NAME': 'heiat',
        'USER': 'omid',
        'PASSWORD': 'omidTheHorse',

    }
}
# DATABASES_LOCAL = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }
STATIC_ROOT_LOCAL = '/home/omid/heiat/static/'
MEDIA_ROOT_LOCAL = '/home/omid/heiat/media/'
