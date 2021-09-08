"""
Django settings for RolAndalucia project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kf3pbtu^18pn1g*dbu@0d9tet$7jzj$m7p3(m%=p#9pq)ifs4$'
if 'DYNO' in os.environ:
    BASEURL = 'https://rol-andalucia.herokuapp.com/'
# SECURITY WARNING: don't run with debug turned on in production!
#if 'DYNO' in os.environ:
DEBUG = False
#else:
DEBUG = True

if 'DYNO' in os.environ:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['localhost', '192.168.0.11', '*']
VERSION = 2

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    'admin_shortcuts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "colorfield",
    'rest_framework',
    'RolAndalucia.apps.RolAndaluciaConfig',
    'martor',
    'treewidget',
]

USE_TZ = True
TIMEZONE = 'Europe/Madrid'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ADMIN_SHORTCUTS = [
    {
        'shortcuts': [
            {
                'url': '/',
                'open_new_window': True,
            },
            {
                'url_name': 'admin:logout',
            },
            # {
            #     'title': 'Users',
            #     'url_name': 'admin:auth_user_changelist',
            #     'count': 'example.utils.count_users',
            # },
            # {
            #     'title': 'Groups',
            #     'url_name': 'admin:auth_group_changelist',
            #     'count': 'example.utils.count_groups',
            # },
            # {
            #     'title': 'Add user',
            #     'url_name': 'admin:auth_user_add',
            #     'has_perms': 'example.utils.has_perms_to_users',
            # },
        ]
    },
    # {
    #     'title': 'CMS',
    #     'shortcuts': [
    #         {
    #             'title': 'Pages',
    #             'url_name': 'admin:index',
    #         },
    #         {
    #             'title': 'Files',
    #             'url_name': 'admin:index',
    #         },
    #         {
    #             'title': 'Contact forms',
    #             'icon': 'columns',
    #             'url_name': 'admin:index',
    #             'count_new': '3',
    #         },
    #         {
    #             'title': 'Products',
    #             'url_name': 'admin:index',
    #         },
    #         {
    #             'title': 'Orders',
    #             'url_name': 'admin:index',
    #             'count_new': '12',
    #         },
    #     ]
    # },
]
ADMIN_SHORTCUTS_SETTINGS = {
    'show_on_all_pages': True,
    'open_new_window': False,
}

ROOT_URLCONF = 'RolAndalucia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'RolAndalucia.contextProcessors.randoms.randoms'
            ],
        },
    },
]

WSGI_APPLICATION = 'RolAndalucia.wsgi.application'

STATIC_URL = 'RolAndalucia/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'RolAndalucia/static')
]
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

LOGIN_URL = "/login"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


if 'DYNO' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'd6sqvol90idoce',
            'USER': 'wypnnjmxwlgtfw',
            'PASSWORD': '26ce190a0bee8b883b17e69c7e1433f8f49e9084343cd34811d08046b8cd1821',
            'HOST': 'ec2-54-217-235-87.eu-west-1.compute.amazonaws.com',
            'PORT': '5432',
        }
    }

DATABASE_ROUTERS = ['RolAndalucia.routers.PrimaryRouter']

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

import django_heroku

django_heroku.settings(locals())

# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',  # to enable/disable imgur/custom uploader.
    'mention': 'false',  # to enable/disable mention
    'jquery': 'true',  # to include/revoke jquery (require for admin default django)
    'living': 'false',  # to enable/disable live updates in preview
}

# To setup the martor editor with label or not (default is False)
MARTOR_ENABLE_LABEL = False

# Imgur API Keys
MARTOR_IMGUR_CLIENT_ID = '0de70c653eaf77c'
MARTOR_IMGUR_API_KEY = '344b8c01481148013443e98262494b7effc16d00'

# Safe Mode
MARTOR_MARKDOWN_SAFE_MODE = True  # default

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = 'martor.utils.markdownify'  # default
MARTOR_MARKDOWNIFY_URL = '/martor/markdownify/'  # default

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    # Custom markdown extensions.
    'martor.extensions.urlize',
    'martor.extensions.del_ins',  # ~~strikethrough~~ and ++underscores++
    'martor.extensions.mention',  # to parse markdown mention
    'martor.extensions.emoji',  # to parse markdown emoji
    'martor.extensions.mdx_video',  # to parse embed/iframe video
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

# Markdown urls
MARTOR_UPLOAD_URL = '/martor/uploader/'  # default
MARTOR_SEARCH_USERS_URL = '/martor/search-user/'  # default

# Markdown Extensions
# MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://www.webfx.com/tools/emoji-cheat-sheet/graphics/emojis/'     # from webfx
MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://github.githubassets.com/images/icons/emoji/'  # default from github
# MARTOR_MARKDOWN_BASE_MENTION_URL = 'https://python.web.id/author/'                                      # please change this to your domain
