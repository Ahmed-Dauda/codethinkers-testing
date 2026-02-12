
from pathlib import Path

from django.conf import settings

from django.contrib.auth import SESSION_KEY
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ✅ this is correct
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # ✅ this is correct


# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-f1btf-a@a!84mjii=$tgdel4$+w5gtmbw3o%7$8n4w+2rntpns'

# Read SECRET_KEY from an environment variable
# SECURITY WARNING: don't run with debug turned on in production!


import environ


env = environ.Env(DEBUG=(bool, False))

# This line should only be used locally
if os.path.exists(os.path.join(BASE_DIR, '.env')):
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env("DEBUG")


SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# PAYSTACK MODE: 'test' or 'live'
PAYSTACK_MODE = env('PAYSTACK_MODE', default='test')

if PAYSTACK_MODE == 'live':
    PAYSTACK_SECRET_KEY = env('PAYSTACK_LIVE_SECRET_KEY')
    PAYSTACK_PUBLIC_KEY = env('PAYSTACK_LIVE_PUBLIC_KEY')
else:
    PAYSTACK_SECRET_KEY = env('PAYSTACK_TEST_SECRET_KEY')
    PAYSTACK_PUBLIC_KEY = env('PAYSTACK_TEST_PUBLIC_KEY')


# wyswyg = ['grappelli', 'filebrowser']
INSTALLED_APPS = [
  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # make sure sites is included
    'users',
    'sms',
    'student',
    'quiz',
    'teacher',
    'sweetify',
    'widget_tweaks',
    'hitcount',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cloudinary',
    'cloudinary_storage',
    'embed_video',
    'xhtml2pdf',
    'tinymce',
    'django_social_share',
    'import_export',
    'mathfilters',
    'webprojects',
    'certificate_stats',
     "django_fastapi",
     'instructor',
    
    
    
# the social providers
    # 'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',
]

BASE_URL = 'https://codethinkers.org'

AUTH_USER_MODEL = 'users.NewUser'
# Application definition
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # existing backend
    'allauth.account.auth_backends.AuthenticationBackend',
)



SOCIAL_AUTH_GOOGLE_KEY = '571775719816-thu9u968v8gpmcuie9ojlb4u0ahig94t.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_SECRET = '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'

# settings.py

# Specify BigAutoField as the default auto field for all models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SOCIAL_AUTH_FACEBOOK_KEY = '416474800140748'
# SOCIAL_AUTH_FACEBOOK_SECRET = '4763331e29fc3703c82ba85f645fe5af'

# django import and export setting
IMPORT_EXPORT_CHUNK_SIZE = 1000 # speed import and export
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = True # you must have permission b4 export
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = True # you must have permission b4 import
IMPORT_EXPORT_SKIP_ADMIN_LOG = True # speed import and export
IMPORT_EXPORT_USE_TRANSACTIONS = True  # import won’t import only part of the data set.

# allauth settings

SITE_ID = 2

# SOCIALACCOUNT_EMAIL_VERIFIATION = False
# ACCOUNT_AUTHENTICATION_METHOD ='username_email'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
# ACCOUNT_USER_MODEL_USERNAME_FIELD = 'user_name'
# ACCOUNT_SESSION_REMEMBER = True

# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
from django.urls import reverse_lazy

ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False

ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

ACCOUNT_FORMS = {'signup': 'users.forms.SimpleSignupForm'}
ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'
ACCOUNT_SIGNUP_REDIRECT_URL = reverse_lazy('account_login')

# ACCOUNT_SIGNUP_REDIRECT_URL = 'sms:homepage'  # or '/'
LOGIN_REDIRECT_URL = 'sms:homepage'
LOGIN_URL = 'account_login'
LOGOUT_REDIRECT_URL = 'account_login'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    }
}

# unused url
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': SOCIAL_AUTH_GOOGLE_KEY ,
            'secret': SOCIAL_AUTH_GOOGLE_SECRET,
            'key': ''
        }
    }
}

# cloudinary settings
# cloud_name = 'ds5l3gqr6'
# api_key = '671667183251344'
# api_secret = 'P5WKA1qweMmd1i4TkU2W_ZY9ZuA'
# secure = True


import cloudinary
import os
import environ

env = environ.Env()
environ.Env.read_env()

cloudinary.config(
    cloud_name = env("CLOUDINARY_CLOUD_NAME"),
    api_key    = env("CLOUDINARY_API_KEY"),
    api_secret = env("CLOUDINARY_API_SECRET"),
    secure     = True
)


CLOUDINARY_URL = env('CLOUDINARY_URL')
DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'


# before the changes
# import cloudinary
# import environ

# env = environ.Env()
# environ.Env.read_env()

# cloudinary.config(
#     cloud_name = env("CLOUDINARY_CLOUD_NAME"),
#     api_key    = env("CLOUDINARY_API_KEY"),
#     api_secret = env("CLOUDINARY_API_SECRET"),
#     secure     = True
# )

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
#     'API_KEY': env("CLOUDINARY_API_KEY"),
#     'API_SECRET': env("CLOUDINARY_API_SECRET"),
# }

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'


# cloudinary.config( 
#   cloud_name = "ds5l3gqr6", 
#   api_key ="671667183251344", 
#   api_secret = "P5WKA1qweMmd1i4TkU2W_ZY9ZuA",
#   secure = True
# )


# email settings

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# EMAIL_HOST_USER = 'codethinkersacademy2@gmail.com'
# EMAIL_HOST_PASSWORD = 'zlht ehfi ivft vzgh'  # Use an App Password
# DEFAULT_FROM_EMAIL = "codethinkersacademy1@gmail.com"


# real codes
# EMAIL_BACKED = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_HOST = 'smtppro.zoho.eu'
# # EMAIL_HOST = 'smtppro.zoho.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False 
# EMAIL_HOST_USER = 'techsupport@esteemlearningcentre.com'
# # EMAIL_HOST_PASSWORD = '0806563624937811Bm.'
# EMAIL_HOST_PASSWORD = 'techSupport@02'
# DEFAULT_FROM_EMAIL = 'techsupport@esteemlearningcentre.com'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ✅ MUST come before Auth
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.BotSignupProtectionMiddleware',  # Your custom middleware

]


MIDDLEWARE += ['users.middleware.UpdateLastActivityMiddleware']

CSRF_COOKIE_SECURE=False

ROOT_URLCONF = 'school.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # ✅ MUST be here
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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



# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
PROJECT_PATH =os.path.dirname(os.path.abspath(__file__))


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

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")



# Font configuration for badge generator
BADGE_FONT = {
    "family": "Poppins",   # Google Font name
    "weights": {
        "title": "Bold",
        "subtitle": "Regular",
        "name": "Bold",
        "course": "SemiBold",
        "score": "Medium",
        "footer": "Italic",
    },
    "sizes": {
        "title": 50,
        "subtitle": 35,
        "name": 50,
        "course": 35,
        "score": 40,
        "footer": 30,
    }
}


# ADDITIONAL SITEs SECURITY
# HTTPS and secure headers

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 3600  # You can increase to 31536000 (1 year) in production
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies and sessions
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# # Optional - block embedding your site in iframes entirely
# SECURE_FRAME_DENY = True  # Already handled by X_FRAME_OPTIONS = 'DENY'

# end of new security

# end of security codes

# ACCOUNT_SIGNUP_REDIRECT_URL= 'settings.LOGOUT_URL'
# django hit count 
# HITCOUNT_KEEP_HIT_ACTIVE = {'seconds': 2}



HITCOUNT_HITS_PER_IP_LIMIT = 0

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # ✅ Dev-only static folder
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    # ✅ For `collectstatic`


# settings.py

X_FRAME_OPTIONS = 'ALLOW-FROM http://127.0.0.1:8000'
# settings.py

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# # Update database configuration from $DATABASE_URL

#production settings for heroku

import dj_database_url
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Detect DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Heroku/Postgres
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True  # only for Postgres
        )
    }
else:
    # Local development with SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


#local development settings
# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=0)
# DATABASES['default'].update(db_from_env)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'fastapidb',
#         'USER': 'fastapiuser',
#         'PASSWORD': 'fastapi37811',  
#         'HOST': 'localhost',   # or your DB server host
#         'PORT': '5432',        # default postgres port
#     }
# }


# CREATE DATABASE fastapidb;
# psql -U postgres -d your_db_name
# CREATE USER fastapiuser WITH PASSWORD 'fastapi37811';
# GRANT ALL PRIVILEGES ON DATABASE fastapidb TO fastapiuser;


# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATIC_URL = '/static/'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# for TinyMCE 
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 700,
    'entity_encoding': "raw",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'plugins': 'link image preview codesample contextmenu table code mathjax',
    'toolbar': (
        'undo redo | styleselect | bold italic | link image | '
        'alignleft aligncenter alignright alignjustify | '
        'bullist numlist outdent indent | table | codesample | mathjax'
    ),
    'theme': 'silver',

    # ✅ Allow pre/code fully
    'extended_valid_elements': 'pre[class|style],code[class|style]',
    'valid_elements': '*[*]',

    # ✅ Protect code blocks so TinyMCE does NOT "parse" inside them
    'protect': [
        r'<!--[\s\S]*?-->',     # HTML comments
        r'<pre[^>]*>[\s\S]*?</pre>',  # Protect <pre>…</pre>
        r'<code[^>]*>[\s\S]*?</code>' # Protect <code>…</code>
    ],

    # ✅ Styling for code blocks
    'content_style': """
        pre code {
            display: block;
            background: #1e1e1e;
            color: #f8f8f2;
            padding: 10px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 14px;
            line-height: 1.5;
            white-space: pre;
            overflow-x: auto;
        }
    """,

    # ✅ Prevent auto <p> wrapping
    'forced_root_block': False,
    'br_in_pre': True,
}

# TINYMCE_DEFAULT_CONFIG = {
#     'height': 360,
#     'width': 700,
#     'entity_encoding': "raw",            # Preserve <, >, & etc.
#     'cleanup_on_startup': True,
#     'custom_undo_redo_levels': 20,
#     'selector': 'textarea',
#     'plugins': 'link image preview codesample contextmenu table code mathjax',
#     'toolbar': (
#         'undo redo | styleselect | bold italic | link image | '
#         'alignleft aligncenter alignright alignjustify | '
#         'bullist numlist outdent indent | table | codesample | mathjax'
#     ),
#     'theme': 'silver',

#     # MathML support
#     'extended_valid_elements': 'math[*],mrow[*],mfrac[*],mi[*],mn[*],mo[*]',
#     'custom_elements': 'math,mrow,mfrac,mi,mn,mo',
#     'content_style': "math, mrow, mfrac, mi, mn, mo",
#     'mathjax': {
#         'lib': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS_HTML',
#         'symbols': {'mathml': True}
#     },
#     'init_instance_callback': '''
#         function (editor) {
#             console.log('Editor is initialized.');
#             editor.on('click', function(e) {
#                 if (e.target.nodeName === 'MATH' || e.target.closest('math')) {
#                     editor.focus();
#                 }
#             });
#         }
#     ''',

#     # Preserve AI-generated paragraphs and lists exactly
#     'forced_root_block': False,          # Disable automatic <p> wrapping
#     'forced_root_block_attrs': {},       
#     'br_in_pre': True,                   # Preserve line breaks in <pre>

#     # Allow all elements and attributes
#     'valid_elements': '*[*]',
#     'valid_children': (
#         '+body[style|link|script|iframe|section],'
#         '+section[div|p],'
#         '+div[math|mrow|mfrac|mi|mn|mo]'
#     ),
# }

# TINYMCE_DEFAULT_CONFIG = {
#     'height': 360,
#     'width': 700,
#     'entity_encoding': "raw",
#     'cleanup_on_startup': True,
#     'custom_undo_redo_levels': 20,
#     'selector': 'textarea',
#     'plugins': 'link image preview codesample contextmenu table code mathjax',
#     'toolbar': 'undo redo | styleselect | bold italic | link image | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | table | codesample | mathjax',
#     'theme': 'silver',

#     # Additional configuration for MathML
#     'extended_valid_elements': 'math[*],mrow[*],mfrac[*],mi[*],mn[*],mo[*]',
#     'custom_elements': 'math,mrow,mfrac,mi,mn,mo',
#     'content_style': "math, mrow, mfrac, mi, mn, mo",
#     'mathjax': {
#         'lib': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS_HTML',
#         'symbols': {'mathml': True}
#     },
#     'init_instance_callback': '''
#         function (editor) {
#             console.log('Editor is initialized.');

#             // Add event listener for MathML elements
#             editor.on('click', function(e) {
#                 if (e.target.nodeName === 'MATH' || e.target.closest('math')) {
#                     editor.focus();
#                 }
#             });
#         }
#     ''',

#     # Prevent wrapping text in <p> tags
#     'forced_root_block': ' ',  # Use <div> instead of <p>
#     'forced_root_block_attrs': {},  # Clears any forced attributes
#     'br_in_pre': True,  # Insert <br> tags instead of wrapping in <p> tags

#     # Allow all elements and attributes
#     'valid_elements': '*[*]',  # Allow all elements
#     'valid_children': '+body[style|link|script|iframe|section],+section[div|p],+div[math|mrow|mfrac|mi|mn|mo]',
# }


TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/r5ebxl5femg5gy8yvid6alg59ohekm45qlmxptc20qeu5jgw/tinymce/6/tinymce.min.js'
TINYMCE_COMPRESSOR = False


# problem of hosting to heroku and solution
# error: failed to push some refs to 'https://git.heroku.com/codethinkers.git'
# git checkout -b master
# git add .
# git commit -m "your commit message"
# git push -u origin master
# git push heroku master

# # solution to django.db.utils.OperationalError: no such table: auth_user
# python manage.py migrate --run-syncdb



# problem: ValueError: Dependency on app with no migrations: users
# solution

# 1. python manage.py makemigrations users
# 2.  python manage.py migrate users

# using ngov to test webhooks

# change the webhook to a test mode in paystack
# login to the ngrov website and copy and paste ngrok config add-authtoken 2SL4rhAyqYBNfeHZvWsCan18Pcz_71B7staheJejM8eL6husJ
# ngrok http 8000 --host-header=rewrite


# migration folder issues

# if table is referencing deleted column, just remove the table from migration folder

# if makemigration is not recognized, do installation of libraries

#ALTER TABLE public.quiz_course DROP COLUMN course_name;
#ALTER TABLE public.quiz_course ADD COLUMN course_name VARCHAR(50) UNIQUE;



# step 1

# begin;
# set transaction read write;
# ALTER TABLE public.quiz_course
# ADD COLUMN course_name VARCHAR(500);
# COMMIT;  

# step 2

# begin;
# set transaction read write;
# ALTER TABLE "public"."quiz_course"
# ALTER COLUMN "course_name" TYPE bigint USING "course_name"::bigint;
# COMMIT;  

# step 3

# inserting relationships

# begin;
# set transaction read write;
# ALTER TABLE "public"."quiz_course"
# ADD CONSTRAINT "quiz_course_course_name_fkey" FOREIGN KEY ("course_name") REFERENCES "public"."sms_courses" ("id");
# COMMIT;  



# step 4
# python manage.py migrate #in the heroku shell