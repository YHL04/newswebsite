"""
Django settings for newswebsite project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

try:
    from auth import *
except ImportError:
    SSHHOST = (os.environ['SSHHOST'])
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    SQLADDRESS = (os.environ['SQLHOST'], 3306)
    LOCALHOST = os.environ['LOCALHOST']
    SQLPASSWORD = os.environ['SQLPASSWORD']
    DBNAME = os.environ['DBNAME']


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b%8ylptw^jo068dd170i_i49m7@^p#6zq^3jbxa_px)0t4#ru@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# set production to false during development
# py manage.py runserver
PRODUCTION = True

ALLOWED_HOSTS = ['127.0.0.1', 'www.aipapernews.com']
CSRF_TRUSTED_ORIGINS = ['https://yhlim04.pythonanywhere.com', 'http://www.aipapernews.com', 'https://www.aipapernews.com']

# Application definition

INSTALLED_APPS = [
    'daphne',
    'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default ModelBackend
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth authentication backend for social authentication
]

LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'APP': {
            'client_id': '1043734398346-llfe70t9phllrcptit10fl4ajngo9pab.apps.googleusercontent.com',  # YOUR_CLIENT_ID
            'secret': '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',  # YOUR_CLIENT_SECRET
            'key': ''
        }
    }
}

ROOT_URLCONF = 'newswebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates/"],
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

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

WSGI_APPLICATION = 'newswebsite.wsgi.application'
ASGI_APPLICATION = 'newswebsite.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# for remote MySQL database for production

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DBNAME,
            'USER': USERNAME,
            'PASSWORD': SQLPASSWORD,
            'HOST': SQLADDRESS[0],
        }
    }
else:
    # for local sqlite3 database for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite',
        }
    }

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'staticfiles/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
