"""
Django settings for refugee_management project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    # Libraries
    "crispy_forms",
    # Apps
    "accounts",
    "frontend",
    "locations",
    "refugee",
    "organization",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "refugee_management.urls"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-US"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True

WSGI_APPLICATION = "refugee_management.wsgi.application"

"""########################################################################
#######             DEPLOYMENT               #####
########################################################################"""

config = dict(os.environ)
SECRET_KEY = config.get("SECRET_KEY")

# Presence of PRODUCTION as environment variable determines
# if its in development or in production.
production = config.get("PRODUCTION")
if production:
    # production settings
    DEBUG = False
    ALLOWED_HOSTS = ["*"]
else:
    # development/test settings
    DEBUG = True
    ALLOWED_HOSTS = []

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.get("DB_NAME"),
        "USER": config.get("DB_USER"),
        "PASSWORD": config.get("DB_PASSWORD"),
        "HOST": config.get("DB_HOST"),
        "PORT": int(config.get("DB_PORT")),
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

"""########################################################################
#######                     Templating                                #####
########################################################################"""

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

"""########################################################################
#######                    MAIL settings                             #####
########################################################################"""

# for local SMTP - FROM email setting
DEFAULT_FROM_EMAIL = "admin@refugeecare.eu"

# SMTP Email server settings
if not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_HOST = config.get("EMAIL_HOST")
    EMAIL_PORT = int(config.get("EMAIL_PORT"))
    EMAIL_HOST_USER = config.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config.get("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True

"""########################################################################
#######             File Handling + Storage                           #####
########################################################################"""

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520

"""########################################################################
#######                             Others                           #####
########################################################################"""

SITE_ID = 1

CSRF_TRUSTED_ORIGINS = ["https://www.refugeecare.eu"]

AUTH_USER_MODEL = "accounts.AccountUser"

CRISPY_TEMPLATE_PACK = "bootstrap4"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/services"
