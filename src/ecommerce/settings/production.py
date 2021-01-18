"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# 현재 settings.py 화일이 있는 위치의 dir 그리고 그 dir이 존재하는 dir이 BASE_DIR 이 된다.
# 즉, src/ecommerce/settings.py 이므로, src 디렉토리가 BASE_DIR 이 된다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e+)z+d@wo8v1+b=60ce*pc1d!^6y-mcx#nuzjs^#)00kk0n5#q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # our apps
    'accounts',
    'addresses',
    'analytics',
    'billing',
    'carts',
    'marketing',
    'products',
    'orders',
    'search',
    'tags',
]

AUTH_USER_MODEL = 'accounts.User' #changes the built-in user model to ours

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

MAILCHIMP_API_KEY = "2ccebe2cbffdf2c61763cda4c1c3722b-us7"
MAILCHIMP_DATA_CENTEER = "us7"
MAILCHIMP_EMAIL_LIST_ID = "a6a50c7f52" # audience id

STRIPE_SECRET_KEY = 'sk_test_51HputmGYYMq5YiSWSw3vJVfkEkMcmXlolnJ2deRBAcxlAlvPvDG1m6VZcE4hTQjA7senoikZ8L3UEu2FMBVjCkg100gmneW7aT'
STRIPE_PUB_KEY = 'pk_test_51HputmGYYMq5YiSWF1KdXYFZuNIgziD9NS6Vxjx3gK6bAGwXukemgwe7iTH7Bqv7NNC2iZO3HaXE70wkq9XX1JnA00hvSlOlSD'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'
LOGOUT_REDIRECT_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# add this
import dj_database_url
db_from_env = dj_database_url.config() # postgresql database in heroku
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# src/commerce와 같은 레벨로 src/static_my_proj에 STATICFILES_DIRS를 둔다. 즉 프로젝트 내에 관리하겠다는 것이다.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_my_proj"),
]

# BASE_DIR인 src디렉토리가 존재하는 디렉토리이니, ecommerce가 된다.
# 즉 BASE_DIR 내가 아니라 동일한 위치에 static_cdn을 만드는것이다. 즉 프로젝트 외부에 그런 화일들이 있다는 뜻이다.
# 요게 실제 화일들이라는 의미이다.
# 그리고, python manage.py collectstatic command를 수행하면,
# 장고lib.contrib.admin쪽에 있는 static화일들이 static_cdn/static_root로 copy된다.
# 또한, STATICFILES_DIRS에 정의된 static화일들도 통째로 static_cdn/static_root로 copy된다.
# 요약하자면, STATIC_ROOT는 copy가 되는 외부 cdn target 위치이며,
# STATICFILES_DIRS 는 프로젝트내에서 관리하는 static file 들의 위치이다, 물론 django admin은 기본으로 copy 된다.(장고 어드민을 사용해야 하니)
# 즉 추후 production에 배포할때 프로젝트 외부의 cdn화일들 잘 관리하라고 collectstatic 명령어를 만들어 준것이다.
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

# https://kirr.co/vklau5

# Let's Encrypt ssl/tls https

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True