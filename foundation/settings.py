"""
Django settings for foundation project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
from os import environ as env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import dj_database_url

# # Silence warnings from ipython/sqlite
import warnings
import exceptions
warnings.filterwarnings("ignore",
                        category=exceptions.RuntimeWarning,
                        module='django.db.backends.sqlite3.base',
                        lineno=58)

DEBUG = env.get('DJANGO_DEBUG', 'true') == 'true'

if DEBUG:
    SECRET_KEY = 'f8pqx#@_x-nv+$m7q7lt^lrmby4ixjms#x*2_sskn9)%t36(!q'
else:
    SECRET_KEY = env.get('DJANGO_SECRET_KEY')

if env.get('DJANGO_EMAIL_DEBUG') == 'true':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = env.get('DJANGO_EMAIL_HOST', 'localhost')
    EMAIL_PORT = env.get('DJANGO_EMAIL_PORT', '25')
    EMAIL_HOST_USER = env.get('DJANGO_EMAIL_USER', 'mail')
    EMAIL_HOST_PASSWORD = env.get('DJANGO_EMAIL_HOST_PASSWORD', 'mail')
    EMAIL_USE_TLS = env.get('DJANGO_EMAIL_USE_TLS', 'true') == 'true'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.get('DJANGO_ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'djangosecure',
    'compressor',
    'twitter_bootstrap',
    'apps.homepage',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'foundation.urls'

WSGI_APPLICATION = 'foundation.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///development.sqlite3')
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Where else to find static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Collection destination for static files.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGIN_REDIRECT_URL = 'homepage'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# Redirect from plain HTTP to HTTPS if not in dev mode
if env.get('DJANGO_SECURE') == 'true':
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 7 * 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_FRAME_DENY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") # Heroku sends this
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
else:
    SECURE_SSL_REDIRECT = False

COMPRESS_OFFLINE = env.get('DJANGO_COMPRESS_OFFLINE') == 'true'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
