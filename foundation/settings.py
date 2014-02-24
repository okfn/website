"""
Django settings for foundation project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import email.utils
import os
from os import environ as env

import dj_database_url
from memcacheify import memcacheify

# Silence warnings from ipython/sqlite
import warnings
import exceptions
warnings.filterwarnings("ignore",
                        category=exceptions.RuntimeWarning,
                        module='django.db.backends.sqlite3.base',
                        lineno=58)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = int(env.get('DJANGO_SITE_ID', 1))

# The people that get emailed when shit breaks
ADMINS = []
django_admins = env.get('DJANGO_ADMINS')
if django_admins:
    for person in django_admins.split(','):
        res = email.utils.parseaddr(person)
        if res != ('', ''):
            ADMINS.append(res)
ADMINS = tuple(ADMINS)

DEBUG = env.get('DJANGO_DEBUG', 'true') == 'true'

if DEBUG:
    SECRET_KEY = 'f8pqx#@_x-nv+$m7q7lt^lrmby4ixjms#x*2_sskn9)%t36(!q'
else:
    SECRET_KEY = env.get('DJANGO_SECRET_KEY')

if env.get('DJANGO_EMAIL_DEBUG') == 'true':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_USE_TLS = env.get('DJANGO_EMAIL_USE_TLS', 'true') == 'true'
    if 'MANDRILL_USERNAME' in env:
        EMAIL_HOST = 'smtp.mandrillapp.com'
        EMAIL_PORT = 587
        EMAIL_HOST_USER = env['MANDRILL_USERNAME']
        EMAIL_HOST_PASSWORD = env['MANDRILL_APIKEY']
    else:
        EMAIL_HOST = env.get('DJANGO_EMAIL_HOST', 'localhost')
        EMAIL_PORT = env.get('DJANGO_EMAIL_PORT', '25')
        EMAIL_HOST_USER = env.get('DJANGO_EMAIL_USER', 'mail')
        EMAIL_HOST_PASSWORD = env.get('DJANGO_EMAIL_HOST_PASSWORD', 'mail')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.get('DJANGO_ALLOWED_HOSTS', '').split(',')

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

    # 3rd-party important
    'djangosecure',
    'south',
    'reversion',
    's3_folder_storage',
    'pagedown',
    'markdown_deux',
    'haystack',

    # Asset pipeline
    'compressor',

    # CMS plugins
    'djangocms_file',
    'djangocms_googlemap',
    'djangocms_picture',
    'djangocms_link',
    'djangocms_text_ckeditor',
    'aldryn_search',

    # CMS
    'cms',
    'mptt',
    'menus',
    'sekizai',

    # Custom apps
    'foundation.djangocms_submenu',
    'foundation.jobs',
    'foundation.press',
    'foundation.organisation',
    'foundation.search',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
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
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
    'lib.context_processors.site',
    'lib.context_processors.google_analytics',
)

ROOT_URLCONF = 'foundation.urls'

WSGI_APPLICATION = 'foundation.wsgi.application'

# Use memcache for django.core.cache if available (see the
# django-heroku-memcacheify documentation for details)
CACHES = memcacheify()

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///development.sqlite3')
}


# Search engine configurations

# NB: simple_backend doesn't play nicely with Django==1.6 due to a known bug:
#
#     https://github.com/toastdriven/django-haystack/issues/908
#
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'
    }
}

haystack_default = HAYSTACK_CONNECTIONS['default']
haystack_engine = env.get('HAYSTACK_SEARCH_ENGINE')

if haystack_engine == 'solr':
    haystack_default['ENGINE'] = 'haystack.backends.solr_backend.SolrEngine'
    haystack_default['URL'] = env.get('HAYSTACK_SOLR_URL')
elif haystack_engine == 'elasticsearch':
    haystack_default['ENGINE'] = \
        'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine'
    haystack_default['URL'] = env.get('HAYSTACK_ELASTICSEARCH_URL')
    haystack_default['INDEX_NAME'] = \
        env.get('HAYSTACK_ELASTICSEARCH_INDEX_NAME')
# Haystack also supports a number of other backends which could be configured
# here.

# Haystack on heroku using Bonsai:
bonsai_url = env.get('BONSAI_URL')
if bonsai_url is not None:
    haystack_default['ENGINE'] = \
        'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine'
    haystack_default['URL'] = bonsai_url
    haystack_default['INDEX_NAME'] = \
        env.get('HAYSTACK_ELASTICSEARCH_INDEX_NAME', 'foundation')

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

if env.get('DJANGO_USE_AWS_STORAGE') == 'true':
    AWS_ACCESS_KEY_ID = env['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = env['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = env['AWS_STORAGE_BUCKET_NAME']
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400',
    }

    STATICFILES_STORAGE = 'lib.cached_storage.CachedStaticStorage'
    STATIC_S3_PATH = 'assets'
    STATIC_ROOT = 'assets/'

    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    MEDIA_ROOT = 'media/'

    if AWS_S3_CUSTOM_DOMAIN:
        STATIC_URL = '//%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATIC_S3_PATH)
        MEDIA_URL = '//%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, DEFAULT_S3_PATH)
    else:
        STATIC_URL = '//s3.amazonaws.com/%s/%s/' % (AWS_STORAGE_BUCKET_NAME,
                                                    STATIC_S3_PATH)
        MEDIA_URL = '//s3.amazonaws.com/%s/%s/' % (AWS_STORAGE_BUCKET_NAME,
                                                   DEFAULT_S3_PATH)

else:
    STATIC_URL = '/assets/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGIN_REDIRECT_URL = 'pages-root'
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

    CSP_DEFAULT_SRC = ("'none'",)

    CSP_SCRIPT_SRC = asset_hosts + ['https://js-agent.newrelic.com',
                                    'https://www.google-analytics.com']
    CSP_STYLE_SRC = asset_hosts + ['https://fonts.googleapis.com',
                                   "'unsafe-inline'"]
    CSP_IMG_SRC = asset_hosts + ['data://']
    CSP_FONT_SRC = asset_hosts + ['https://netdna.bootstrapcdn.com',
                                  'https://themes.googleusercontent.com']

    CSP_REPORT_URI = env.get('DJANGO_CSP_REPORT_URI')

GOOGLE_ANALYTICS_TRACKING_ID = env.get('DJANGO_GOOGLE_ANALYTICS_TRACKING_ID')
GOOGLE_ANALYTICS_DOMAIN = env.get('DJANGO_GOOGLE_ANALYTICS_DOMAIN')

if env.get('DJANGO_USE_AWS_STORAGE') == 'true':
    COMPRESS_STORAGE = 'lib.cached_storage.CachedStaticStorage'

COMPRESS_OFFLINE = env.get('DJANGO_COMPRESS_OFFLINE') == 'true'
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'GOOGLE_ANALYTICS_TRACKING_ID': GOOGLE_ANALYTICS_TRACKING_ID,
    'GOOGLE_ANALYTICS_DOMAIN': GOOGLE_ANALYTICS_DOMAIN,
}

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lib.precompilers.LessFilter'),
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter'
]

CMS_TEMPLATES = (
    ('cms_default.html', 'Default layout'),
    ('cms_twocolumn.html', 'Two columns'),
    ('cms_threecolumn.html', 'Three columns'),
    ('cms_homepage.html', 'Homepage'),
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
