from .base import *
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
SETTINGS_DIR = os.path.join(BASE_DIR, 'avastove', 'settings')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'local_settings.json')

with open(SETTINGS_FILE) as f:
    settings_json = json.loads(f.read())

SECRET_KEY = settings_json['django_settings']['key']

DEBUG = True

ALLOWED_HOSTS = '*'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'storages',
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
'''
#### Static settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')#이 폴더가 없으면 만들어질 것이다.

#### Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_dir')

'''
# -------------------------------------------------------------------
# Static settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = settings_json['cdn']['aws']['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = settings_json['cdn']['aws']['aws_secret_access_key']
AWS_STORAGE_BUCKET_NAME = settings_json['cdn']['aws']['aws_storage_bucket_name']
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': settings_json['cdn']['aws']['aws_s3_object_parameters']['cachecontrol'],
}

AWS_S3_CUSTOM_DOMAIN = 'cf.sajufortune.com'

# Static Setting
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Media Setting
MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN

# -------------------------------------------------------------------



SMTPusername = settings_json['django']['SMTPusername']
SMTPpassword = settings_json['django']['SMTPpassword']


# Email-backend
EMAIL_BACKEND = settings_json['django']['email_backend']
EMAIL_HOST = settings_json['django']['email_host']
EMAIL_PORT = 587
EMAIL_HOST_USER = SMTPusername
EMAIL_HOST_PASSWORD = SMTPpassword
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = settings_json['django']['default_from_email']

# aws workmail 사용

