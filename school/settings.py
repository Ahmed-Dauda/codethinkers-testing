"""
Django settings for school project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-f1btf-a@a!84mjii=$tgdel4$+w5gtmbw3o%7$8n4w+2rntpns'

# Read SECRET_KEY from an environment variable
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['codethinkers.herokuapp.com','codethinkerslms.com','www.codethinkerslms.com','codethinkers.org','www.codethinkers.org', '127.0.0.1']
# ALLOWED_HOSTS = ['ctsaalms.herokuapp.com','codethinkers.org' ,'127.0.0.1']

# Application definition
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # existing backend
    'allauth.account.auth_backends.AuthenticationBackend',
)
AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'sms',
    'users',
    'sweetify',
    'widget_tweaks',
    'hitcount',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # make sure sites is included
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',

# the social providers
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',
]

# SOCIAL_AUTH_GOOGLE_KEY = '571775719816-thu9u968v8gpmcuie9ojlb4u0ahig94t.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_SECRET = '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'

# SOCIAL_AUTH_FACEBOOK_KEY = '416474800140748'
# SOCIAL_AUTH_FACEBOOK_SECRET = '4763331e29fc3703c82ba85f645fe5af'

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }

# allauth setting
SITE_ID = 1

# SOCIALACCOUNT_PROVIDERS = {
#     'facebook': {
#         'METHOD': 'oauth2',
#         'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
#         'SCOPE': ['email', 'public_profile'],
#         'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
#         'INIT_PARAMS': {'cookie': True},
#         'FIELDS': [
#             'id',
#             'first_name',
#             'last_name',
#             'middle_name',
#             'name',
#             'name_format',
#             'picture',
#             'short_name'
#         ],
#         'EXCHANGE_TOKEN': True,
#         'LOCALE_FUNC': 'path.to.callable',
#         'VERIFIED_EMAIL': False,
#         'VERSION': 'v7.0',
#     }
# }

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'



# email settings
# EMAIL_BACKED = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'codethinkers.org'
# EMAIL_PORT =465
# EMAIL_HOST_USER= 'no-reply@domain.com'
# EMAIL_HOST_PASSWORD = '0806563624937811'
# EMAIL_USER_TLS = False
# EMAIL_USER_SSL = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# origin code

# SENDGRID_API_KEY = os.environ["apikey"]
# SENDGRID_PASSWORD= os.environ["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"]
# SENDGRID_USERNAME= os.environ["codethinkers"]

# EMAIL_BACKED = 'django.core.mail.backends.smtp.EmailBackend'
# # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT =587
# EMAIL_HOST_USER = 'apikey' 
# EMAIL_HOST_PASSWORD = SENDGRID_PASSWORD
# EMAIL_USER_TLS = False
# EMAIL_USER_SSL = True
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# ps = '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'
# server ='smtp.sendgrid.net'
# ports ='25, 587 465'
# un='apikey'
# EHU='codethinkers'
# EMAIL_HOST_USER=mitchelltabian@gmail.com
# EMAIL_HOST_PASSWORD=your_app_password_here

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'securesally@gmail.com'
# EMAIL_HOST_PASSWORD = 'olfxieyveruumqrx'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'CodingWithMitch Team <noreply@codingwithmitch.com>'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'school.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURE_SSL_REDIRECT = True

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'
# LOGOUT_REDIRECT_URL = 'signupview'

# django hit count 
HITCOUNT_KEEP_HIT_ACTIVE = {'seconds': 2}

HITCOUNT_HITS_PER_IP_LIMIT = 0

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT =os.path.join(BASE_DIR, 'static')
MEDIA_ROOT =os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Heroku: Update database configuration from $DATABASE_URL.

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
# db_from_env = dj_database_url.config(default='postgre://...')
DATABASES['default'].update(db_from_env)


STATIC_ROOT = BASE_DIR / 'staticfiles'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
