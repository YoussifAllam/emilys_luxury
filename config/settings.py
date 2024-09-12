"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY = 'django-insecure-*tifw%5#mu*9=1re=3v8&=^1w0v2c6c60^3l(5*s4$f9k_i*38'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

GOOGLE_API_KEY='AIzaSyBJC3g77500BWL2I76rcgdwW4sSDY-idWo'
GOOGLE_CSE_ID='4223bc263001c4618'

GOOGLE_OAUTH2_CLIENT_ID='135222470649-vgr2d50scr63a617pui2tntcho585jr9.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET='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'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_AGE = 3600 
SESSION_COOKIE_SECURE = False  
SESSION_COOKIE_HTTPONLY = True  

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '135222470649-vgr2d50scr63a617pui2tntcho585jr9.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


ALLOWED_HOSTS = ['*']


# Application definition




DEFAULT_APPS = [
    
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.simple_history",
    'multi_captcha_admin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS =[
    'allauth',
    'allauth.account',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'corsheaders',
    'django_celery_beat',

    # 'tinymce',
    'django_ckeditor_5',
    'captcha',
    'image_uploader_widget',
    'simple_history',
    'django_object_actions',

]


LOCAL_APPS =[
'apps.Users' , 
'apps.Dresses' , 
'apps.investment' , 
'apps.CustomerReviews' , 
'apps.Cart' , 
'apps.Shipping' ,
'apps.Coupons' ,
'apps.FAQ_and_terms' ,
'apps.orders' ,
'apps.Payment',
'apps.SiteOwner_receivable',
'apps.invitation' ,
'apps.Dashboard',
'apps.Captcha_app'

]

MULTI_CAPTCHA_ADMIN = {
    'engine': 'simple-captcha',
}

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydatabase',
#         'USER': 'myuser',
#         'PASSWORD': 'mypassword',
#         'HOST': '185.97.146.60',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#!______________________________________________________-

DEBUG = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



AUTH_USER_MODEL = 'Users.User'

from datetime import timedelta
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     BASE_DIR / "static"
#     ]
STATIC_ROOT  =  BASE_DIR / "static_root"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'Users.User'

OTP_CODE_LENGTH = 6

OTP_CODE_TIMEOUT = 300 # in seconds (5 minutes)



SOCIALACCOUNT_LOGIN_ON_GET=True




DJANGO_BASE_BACKEND_URL="http://localhost"
DJANGO_BASE_FRONTEND_URL="http://localhost:3000"




CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL =True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'https://backend.emilysluxury.com',
]

CSRF_TRUSTED_ORIGINS = ['https://backend.emilysluxury.com']


CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',  # Ensure this is included
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    "Access-Control-Allow-Origin",
]
CORS_ALLOWED_ORIGINS = [
    'https://backend.emilysluxury.com',  # Your frontend URL
]

CSRF_TRUSTED_ORIGINS = ['https://backend.emilysluxury.com']


import environ

# Initialize environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Use the environment variable
TEST_MODE = env('TEST_MODE')

if TEST_MODE == 'True':
    PUBLISHABLE_KEY = env('TEST_Publishable_Key')
    SECRET_KEY = env('TEST_SECRET_KEY')
    CALLBACKURL = env('TEST_CALLBACKURL')
else :
    PUBLISHABLE_KEY = env('LIVE_Publishable_Key')
    SECRET_KEY = env('LIVE_SECRET_KEY')
    CALLBACKURL = env('LIVE_CALLBACKURL')

# print(Publishable_Key , "\n" , SECRET_KEY , "\n" , CALLBACKURL)


# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'


# from .logger_config import   *
from .send_email_config import *
from .Tinymce_config import *
from .CKEDITOR5_config import *