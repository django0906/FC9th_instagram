"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')


# 사용자가 업로드한 파일이 저장될 base dir(settings.MEDIA_ROOT)
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
# 유저가 업로드한 파일에 접근하고자 할 때(settings.MEDIA_URL)
MEDIA_URL = '/media/'
# 이 값은 settings.STATIC_URL
# STATICFILES_DIRS에 있는 파일목록을 검색
# 있으면 해당 파일을 response
STATIC_URL = '/static/'

# 정적파일 검색 경로 목록
STATICFILES_DIRS = [
    STATIC_DIR,
]

secrets = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))
FACEBOOK_APP_ID = secrets['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET = secrets['FACEBOOK_APP_SECRET']

# login_required 데코레이터에 의해 로그인 페이지로 이동해야할 때,
# 그 이동할 URL 또는 URL 패턴 이름
LOGIN_URL = 'members:login_view'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.FacebookBackend',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Auth
AUTH_USER_MODEL = 'members.User'

# Application definition

INSTALLED_APPS = [
    'members.apps.MembersConfig',
    # 이런 방식으로 앱 추가하는것이 훨씬 권장된다!
    'posts.apps.PostsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ]
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

WSGI_APPLICATION = 'config.wsgi.application'

# 템플릿에서 message.tags에 사용될 값 커스터마이징
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True



