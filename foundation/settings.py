"""
Django settings for foundation project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import environ
import os
import sys
import email.utils
from os import environ as env
from django.utils.translation import gettext_lazy as _
import warnings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEST_MODE = len(sys.argv) > 1 and 'test' in sys.argv

djenv = environ.Env()
# Base settings are common to all environments
env_file = os.path.join(BASE_DIR, ".env.base")
djenv.read_env(env_file, overwrite=True)

# try google secrets file
google_secrets_file = '/secrets/django_settings'
if os.path.isfile(google_secrets_file):
    # we are in google environment
    extra_env_file = google_secrets_file
elif TEST_MODE:
    # we are in test environment
    extra_env_file = os.path.join(BASE_DIR, ".env.test")
else:
    # We are runnign a local instance
    extra_env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(extra_env_file):
    djenv.read_env(extra_env_file, overwrite=True)

# Silence warnings from ipython/sqlite
warnings.filterwarnings("ignore",
                        category=RuntimeWarning,
                        module='django.db.backends.sqlite3.base',
                        lineno=58)


SITE_ID = int(env.get('DJANGO_SITE_ID', 1))


def _parse_email_list(varname):
    people = []
    emails = env.get(varname)
    if emails:
        for person in emails.split(','):
            res = email.utils.parseaddr(person)
            if res != ('', ''):
                people.append(res)
    return tuple(people)


# The people that get emailed when shit breaks (500)
ADMINS = _parse_email_list('DJANGO_ADMINS')

# The people that get emailed when shit is missing (404)
MANAGERS = _parse_email_list('DJANGO_MANAGERS')

DEBUG = env.get('DJANGO_DEBUG', 'true') == 'true'

if DEBUG:
    SECRET_KEY = 'f8pqx#@_x-nv+$m7q7lt^lrmby4ixjms#x*2_sskn9)%t36(!q'
    X_FRAME_OPTIONS = "SAMEORIGIN"
else:
    SECRET_KEY = env.get('DJANGO_SECRET_KEY')

if env.get('DJANGO_EMAIL_DEBUG') == 'true':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_USE_TLS = env.get('DJANGO_EMAIL_USE_TLS', 'true') == 'true'
    EMAIL_HOST = env.get('DJANGO_EMAIL_HOST', 'localhost')
    EMAIL_HOST_USER = env.get('DJANGO_EMAIL_HOST_USER', 'mail')
    EMAIL_HOST_PASSWORD = env.get('DJANGO_EMAIL_HOST_PASSWORD', 'mail')
    EMAIL_PORT = env.get('DJANGO_EMAIL_PORT', '25')

# Contact Form (sendemail app)
CONTACT_EMAIL_SENDER = env.get('CONTACT_EMAIL_SENDER')
GENERAL_EMAIL_RECEPIENTS = _parse_email_list('GENERAL_EMAIL_RECEPIENTS')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
DEFAULT_FROM_EMAIL = 'noreply@localhost'
SERVER_EMAIL = 'admin-noreply@localhost'
if env.get('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS = env.get('DJANGO_ALLOWED_HOSTS').split(',')
    DEFAULT_FROM_EMAIL = 'noreply@%s' % ALLOWED_HOSTS[0]
    SERVER_EMAIL = 'admin-noreply@%s' % ALLOWED_HOSTS[0]

INSTALLED_APPS = (
    # CMS admin theme
    'djangocms_admin_style',

    # Django core
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.redirects',  # Provides redirects app
    'django.forms',  # Required to override django-simple-captcha template

    # 3rd-party important
    'reversion',
    'pagedown',
    'markdown_deux',
    'haystack',
    'sendemail',
    'captcha',

    # Asset pipeline
    'compressor',

    # CMS plugins
    'djangocms_file',
    'djangocms_picture',
    'djangocms_link',
    'djangocms_text_ckeditor',
    'aldryn_video',
    'aldryn_quote',
    'easy_thumbnails',
    'filer',

    # CMS
    'cms',
    'mptt',
    'treebeard',
    'menus',
    'sekizai',

    # Custom apps
    'foundation.features',
    'foundation.jobs',
    'foundation.organisation',
    'foundation.search',
    'foundation.okfplugins.header',
    'foundation.okfplugins.heading',
    'foundation.okfplugins.just_text',
    'foundation.okfplugins.article_link',
    'foundation.okfplugins.grid_columns',
    'foundation.okfplugins.pill_button',
    'foundation.okfplugins.pills_menu',
    'foundation.okfplugins.banner',
    'foundation.okfplugins.video',
    'foundation.okfplugins.full_banner',
    'foundation.okfplugins.image',
    'foundation.okfplugins.feature_block',
    'foundation.okfplugins.newsletter',
    'foundation.okfplugins.gallery',
    'foundation.okfplugins.blog_opening',
    'foundation.okfplugins.hero_punch',
    'foundation.okfplugins.spotlight',
    'foundation.okfplugins.quote',
    'foundation.okfplugins.carousel',
    'foundation.okfplugins.list',
    'foundation.okfplugins.content_list',
    'foundation.okfplugins.number_stat',
    'article_list_item'
)

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "cms.context_processors.cms_settings",
                "sekizai.context_processors.sekizai",
                "lib.context_processors.site",
                "django.template.context_processors.request",
            ),
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'foundation.urls'
WSGI_APPLICATION = 'foundation.wsgi.application'

# Cache configuration

CACHE_URL = env.get('CACHE_URL')
if not CACHE_URL:
    CACHES = {
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
    }
elif CACHE_URL.startswith('redis://'):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": CACHE_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
elif CACHE_URL.upper() == 'DB':
    # Database cache
    # Requires python manage.py createcachetable
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": env.get('CACHE_DB_TABLE_NAME', 'django_cache_table'),
        }
    }
elif CACHE_URL.upper() == 'FILE':
    # File system cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_fs_cache',
        }
    }

# Database configuration

DATABASES = {
    'default': {
        'ENGINE': env.get('DB_ENGINE'),
        'NAME': env.get('DB_NAME'),
        'USER': env.get('DB_USER'),
        'PASSWORD': env.get('DB_PASSWORD'),
        'HOST': env.get('DB_HOST'),
        'PORT': env.get('DB_PORT'),
    },
}

if not DEBUG:
    # Keep database connections around for a while, reusing them when possible.
    CONN_MAX_AGE = 60

# Search configuration

# Use realtime updates (synchronously update the index on model save/delete)
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
]

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

CUSTOM_ASSETS_DOMAIN = env.get('DJANGO_CUSTOM_ASSETS_DOMAIN')

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if env.get('DJANGO_USE_GOOGLE_STORAGE') == 'true':
    GS_BUCKET_NAME = env.get("GS_BUCKET_NAME", "django-statics-okf-website-staging")
    GS_PROJECT_ID = env.get("GS_PROJECT_ID")
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    THUMBNAIL_DEFAULT_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_QUERYSTRING_AUTH = False
    GS_DEFAULT_ACL = "publicRead"
    # We use local static files, not use STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Flag directory (uses flags from Open Icon Library)
COUNTRIES_FLAG_URL = '/assets/img/flags/png/flag-{code}.png'

# Override country names in django_countries
COUNTRIES_OVERRIDE = {
    'TW': _('Taiwan'),
    'IR': _('Iran'),
    'KR': _('South Korea'),
    'AB': _('Scotland'),
}

LOGIN_REDIRECT_URL = 'pages-root'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# Redirect from plain HTTP to HTTPS if not in dev mode
if env.get('DJANGO_SECURE') == 'true':
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 7 * 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # Heroku sends this
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
else:
    SECURE_SSL_REDIRECT = False

# Content Security Policy
asset_hosts = ['https://storage.googleapis.com']
if CUSTOM_ASSETS_DOMAIN:
    asset_hosts.append('https://%s' % CUSTOM_ASSETS_DOMAIN)

CSP_DEFAULT_SRC = ("'self'",)

CSP_SCRIPT_SRC = asset_hosts + [
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    'https://js-agent.newrelic.com',
    'https://use.typekit.net',
    'https://bam.nr-data.net',
    'https://downloads.mailchimp.com',
    'https://s3.amazonaws.com/downloads.mailchimp.com',
    '*.list-manage.com',
    'https://youtube.com',
    'https://www.youtube.com',
    'https://plausible.io',
]
CSP_STYLE_SRC = asset_hosts + [
    "'self'",
    "'unsafe-inline'",
    'https://use.typekit.net',
    'https://downloads.mailchimp.com',
]
CSP_IMG_SRC = asset_hosts + [
    "'self'",
    "data:",
    'https://gravatar.com',
    'https://1.gravatar.com',
    'https://2.gravatar.com',
    'https://secure.gravatar.com',
    'https://p.typekit.net',
    'https://ping.typekit.net',
    'https://cdn-images.mailchimp.com',
    'https://paypal.com',
    'https://www.paypal.com',
    'https://paypalobjects.com',
    'https://www.paypalobjects.com',
]
CSP_FONT_SRC = asset_hosts + [
    "'self'",
    'data:',
    'https://use.typekit.net',
    'https://themes.googleusercontent.com',
    'https://fonts.gstatic.com',
]
CSP_FORM_ACTION = [
    "'self'",
    'https://okfn.us9.list-manage.com',
    'https://paypal.com',
    'https://www.paypal.com',
]
CSP_FRAME_SRC = [
    "'self'",
    'https://youtube.com',
    'https://www.youtube.com',
]
CSP_CONNECT_SRC = asset_hosts + [
    "'self'",
    'https://plausible.io',
]
# Report-URI is no longer recommended
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-uri
# CSP_REPORT_URI = env.get('DJANGO_CSP_REPORT_URI')
# CSP_REPORT_ONLY = True

COMPRESS_OFFLINE = env.get('DJANGO_COMPRESS_OFFLINE') == 'true'
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
}

COMPRESS_PRECOMPILERS = (
    ('text/sass', 'lib.precompilers.SassFilter'),
)

COMPRESS_FILTERS = {
    'css': ['compressor.filters.cssmin.CSSMinFilter']
}

CMS_CACHE_DURATIONS = {
    'content': 60,
    'menus': 3600,
    'permissions': 3600,
}

CMS_COLOR_SCHEME = "light"
CMS_COLOR_SCHEME_TOGGLE = True

CMS_TEMPLATES = (
    ('cms_default.html', 'Default layout'),
    ('cms_twocolumn.html', 'Two columns'),
    ('cms_homepage.html', 'Homepage'),
    ('cms_landing.html', 'Landing'),
    ('cms_article.html', 'Article'),
    ('cms_childlist.html', 'Child list'),
    ('cms_contact.html', 'Contact'),
)

# Allow iframes in the cms text plugin
TEXT_ADDITIONAL_TAGS = ('iframe',)

THUMBNAIL_DEBUG = DEBUG  # easy-thumbnails debugging

QUOTE_STYLES = (
    'carousel',
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CAPTCHA_IMAGE_SIZE = (150, 75)
CAPTCHA_FONT_SIZE = 44


if TEST_MODE:
    from .test_settings import *  # noqa
