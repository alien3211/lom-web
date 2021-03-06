"""
Django settings for lom project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from configurations import Configuration
from django.core.urlresolvers import reverse_lazy

import hashlib
import os
import uuid

def get_secret_key(base_dir='.'):
    def get_key(key_path):
        with open(key_path, 'w') as key_file:
            key = hashlib.sha512(str(uuid.uuid4()).encode('utf8')).hexdigest()
            key_file.write(key)
        return key

    path = os.path.join(base_dir, '.secret.key')

    try:
        secret_key = open(path).read()
        assert secret_key, "Wrong secret key"
    except (IOError, AssertionError):
        secret_key = get_key(path)
    return secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Production(Configuration):
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = get_secret_key(BASE_DIR)

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['172.0.0.1', 'localhost']


    # Application definition

    INSTALLED_APPS = [
        'posts',
        'comments',
        #####################
        'bootstrap3',
        'crispy_forms',

        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # 'allauth.socialaccount.providers.facebook',

        'categories',
        'categories.editor',

        'taggit',
        'pagedown',

        'haystack',
        #####################
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.sitemaps',
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

    ROOT_URLCONF = 'lom.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'templates'),
            ],
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

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
    )


    WSGI_APPLICATION = 'lom.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/1.10/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/1.10/topics/i18n/

    LANGUAGE_CODE = 'pl'

    TIME_ZONE = 'Europe/Warsaw'

    USE_I18N = True # internationalization

    USE_L10N = True # localization

    USE_TZ = True # time zone

    # AUTH_USER_MODEL = 'users.BiblioUser'


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

    MEDIA_URL = '/media/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    SITE_ID = 1  # because enable django.contrib.sites

    # Bootstrap3

    BOOTSTRAP3 = [

    ]

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

    # allauth config
    LOGIN_REDIRECT_URL = 'posts:list'
    LOGIN_URL = 'posts:list'
    ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy('posts:list')


    POST_PER_PAGE = 5

    # Haystack

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://127.0.0.1:8983/solr/posts'
        },
    }


class Dev(Production):
    DEBUG = True

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # send email to console output

    CATEGORIES_SETTINGS = {
        'M2M_REGISTRY': {
            'app.AModel': 'categories',
            'app.MyModel': (
                {'name': 'other_categories', 'related_name': 'other_cats'},
                {'name': 'more_categories', 'related_name': 'more_cats'},
            ),
        }
    }