MEDIA_ROOT_LOCAL= './'
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
STATIC_ROOT_LOCAL='/home/omid/static'