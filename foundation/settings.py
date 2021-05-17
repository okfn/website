"""
Django settings for foundation project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys
import email.utils
from os import environ as env
import dj_database_url
from django.utils.translation import ugettext_lazy as _
from dotenv import load_dotenv
import warnings

TEST_MODE = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Activate dotenv
if not TEST_MODE:
    load_dotenv('.env')

# Silence warnings from ipython/sqlite
warnings.filterwarnings("ignore",
                        category=RuntimeWarning,
                        module='django.db.backends.sqlite3.base',
                        lineno=58)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = int(env.get('DJANGO_SITE_ID', 1))
HUBOT_API_KEY = env.get('HUBOT_API_KEY')


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

# set default email sender account for contact form enquiries
CONTACT_EMAIL_SENDER = env.get('CONTACT_EMAIL_SENDER')

# accounts that receive various enquiries from contact forms
PRESS_EMAIL_RECEPIENTS = _parse_email_list('PRESS_EMAIL_RECEPIENTS')
SERVICE_EMAIL_RECEPIENTS = _parse_email_list('SERVICE_EMAIL_RECEPIENTS')
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

    # 3rd-party important
    'reversion',
    's3_folder_storage',
    'pagedown',
    'markdown_deux',
    'haystack',
    'spurl',
    'standard_form',
    'formtools',
    'sendemail',

    # Asset pipeline
    'compressor',

    # CMS plugins
    'djangocms_file',
    'djangocms_picture',
    'djangocms_link',
    'djangocms_text_ckeditor',
    'aldryn_search',
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
    'foundation.blogfeed',
    'foundation.features',
    'foundation.jobs',
    'foundation.press',
    'foundation.organisation',
    'foundation.search',
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
                "lib.context_processors.google_analytics",
                "lib.context_processors.mailchimp",
                "django.template.context_processors.request",
            ),
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "aldryn_boilerplates.template_loaders.AppDirectoriesLoader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ALDRYN_BOILERPLATE_NAME = 'bootstrap3'
ROOT_URLCONF = 'foundation.urls'
WSGI_APPLICATION = 'foundation.wsgi.application'

# Cache configuration

CACHE_URL = env.get('CACHE_URL')
if CACHE_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": CACHE_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
else:
    CACHES = {
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
    }

# Database configuration

db_config = dj_database_url.config(default='sqlite:///development.sqlite3')
DATABASES = {
    'default': db_config
}

if not DEBUG:
    # Keep database connections around for a while, reusing them when possible.
    CONN_MAX_AGE = 60

# Search configuration

# Use realtime updates (synchronously update the index on model save/delete)
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
SEARCH_URL = env.get('SEARCH_URL')
if SEARCH_URL:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': SEARCH_URL,
            'INDEX_NAME': 'foundation',
        }
    }
else:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), '..', 'whoosh_index'),
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

AWS_S3_CUSTOM_DOMAIN = env.get('DJANGO_AWS_S3_CUSTOM_DOMAIN')

CUSTOM_ASSETS_DOMAIN = env.get('DJANGO_CUSTOM_ASSETS_DOMAIN')

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if env.get('DJANGO_USE_AWS_STORAGE') == 'true':
    AWS_ACCESS_KEY_ID = env['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = env['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = env['AWS_STORAGE_BUCKET_NAME']
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'

    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    THUMBNAIL_DEFAULT_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    MEDIA_ROOT = 'media/'

    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = '//%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, DEFAULT_S3_PATH)
    else:
        MEDIA_URL = '//s3.amazonaws.com/%s/%s/' % (AWS_STORAGE_BUCKET_NAME,
                                                   DEFAULT_S3_PATH)
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
if env.get('DJANGO_CSP_REPORT_URI') is not None:
    CSP_REPORT_ONLY = True

    asset_hosts = []
    if AWS_S3_CUSTOM_DOMAIN:
        asset_hosts.append('https://%s' % AWS_S3_CUSTOM_DOMAIN)
    else:
        asset_hosts.append('https://s3.amazonaws.com')
    if CUSTOM_ASSETS_DOMAIN:
        asset_hosts.append('https://%s' % CUSTOM_ASSETS_DOMAIN)

    CSP_DEFAULT_SRC = ("'none'",)

    CSP_SCRIPT_SRC = asset_hosts + [
        "'self'",
        "'unsafe-inline'",
        'https://js-agent.newrelic.com',
        'https://www.google-analytics.com',
        'https://use.typekit.net',
        'https://bam.nr-data.net',
        'https://downloads.mailchimp.com',
        'https://s3.amazonaws.com/downloads.mailchimp.com',
        '*.list-manage.com',
    ]
    CSP_STYLE_SRC = asset_hosts + [
        "'self'",
        "'unsafe-inline'",
        'https://use.typekit.net',
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
        'https://www.google-analytics.com',
    ]
    CSP_FONT_SRC = asset_hosts + [
        "'self'",
        'data:',
        'https://use.typekit.net',
        'https://themes.googleusercontent.com'
    ]
    CSP_FORM_ACTION = [
        "'self'",
        'https://okfn.us9.list-manage.com'
    ]

    CSP_REPORT_URI = env.get('DJANGO_CSP_REPORT_URI')
else:
    CSP_EXCLUDE_URL_PREFIXES = ('/',)

GOOGLE_ANALYTICS_TRACKING_ID = env.get('DJANGO_GOOGLE_ANALYTICS_TRACKING_ID')
GOOGLE_ANALYTICS_DOMAIN = env.get('DJANGO_GOOGLE_ANALYTICS_DOMAIN')

MAILCHIMP_URL = env.get('DJANGO_MAILCHIMP_URL', '')
MAILCHIMP_TOKEN = env.get('DJANGO_MAILCHIMP_TOKEN', '')

COMPRESS_OFFLINE = env.get('DJANGO_COMPRESS_OFFLINE') == 'true'
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'GOOGLE_ANALYTICS_TRACKING_ID': GOOGLE_ANALYTICS_TRACKING_ID,
    'GOOGLE_ANALYTICS_DOMAIN': GOOGLE_ANALYTICS_DOMAIN,
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

CMS_TEMPLATES = (
    ('cms_default.html', 'Default layout'),
    ('cms_twocolumn.html', 'Two columns'),
    ('cms_homepage.html', 'Homepage'),
    ('cms_landing.html', 'Landing'),
    ('cms_article.html', 'Article'),
    ('cms_childlist.html', 'Child list'),
    ('cms_contact.html', 'Contact'),
)

CMS_PLACEHOLDER_CONF = {
    # The 'blurb' placeholder is only intended to take text. To minimise the
    # chance of screwing up page layout, restrict the placeholder to only
    # accept the text plugin.
    'blurb': {
        'plugins': ['TextPlugin'],
        'text_only_plugins': ['LinkPlugin']
    },
}

# Allow iframes in the cms text plugin
TEXT_ADDITIONAL_TAGS = ('iframe',)

THUMBNAIL_DEBUG = DEBUG  # easy-thumbnails debugging

QUOTE_STYLES = (
    'carousel',
)

if TEST_MODE:
    from .test_settings import *  # noqa
