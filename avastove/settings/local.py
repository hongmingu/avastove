from .base import *
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
SETTINGS_DIR = os.path.join(BASE_DIR, 'avastove', 'settings')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'local_settings.json')

with open(SETTINGS_FILE) as f:
    settings_json = json.loads(f.read())

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'imagekit',
    'authapp',
    'baseapp',
    'debug_toolbar',
    'object',
    'relation',
    'notice',
]
# django debug-toolbar
INTERNAL_IPS = ('127.0.0.1',)

SITE_ID = 1


WSGI_APPLICATION = 'avastove.wsgi.local.application'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django debug-toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'avastove.urls'

# Authentication Backend
AUTHENTICATION_BACKENDS = [
    'authapp.backends.EmailOrUsernameAuthBackend',
    # 'django.contrib.auth.backends.ModelBackend',
]

#### Static settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')#이 폴더가 없으면 만들어질 것이다.

#### Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_dir')


SMTPusername = settings_json['django']['SMTPusername']
SMTPpassword = settings_json['django']['SMTPpassword']


# Email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = SMTPusername
EMAIL_HOST_PASSWORD = SMTPpassword
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'test-username@moneycurry.com'

# aws workmail 사용
#########################reCAPTCHA#############################

GOOGLE_RECAPTCHA_SECRET_KEY = '6Ld4Tz4UAAAAALpirKbseTu8m01Afd6Fr-fW5OBy'

#---------------------channels-----------------------
# Channel layer definitions
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation channels_redis
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [(redis_host, 6379)],
            "hosts": [('redis://127.0.0.1:6379')],
        },
    },
}



# ASGI_APPLICATION should be set to your outermost router
ASGI_APPLICATION = 'avastove.routing.application'

# Cache (It's different from channels)
'''
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis-test-cache.tegk2s.0001.usw2.cache.amazonaws.com:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
'''
