# Django settings for mainiti project.
import os
from decimal import Decimal

from django.conf import global_settings
from django.core.urlresolvers import reverse_lazy
import dirs


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Turbosys Developers', 'dev@turbosys.com.br'),
)

INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = (
    'mainiti.net.br',
)

EMAIL_SUBJECT_PREFIX = '[Mainiti]'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(dirs.PROJECT_DIR, 'database.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DEFAULT_FROM_EMAIL = 'Mainiti <mainiti@mainiti.net.br>'
SERVER_EMAIL = 'Webmaster Mainiti <webmaster@mainiti.net.br>'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(dirs.PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(dirs.PROJECT_DIR, 'site-static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(dirs.APP_DIR, 'static'),
)

# Path for the docs, to be acessible through debug. In production environment,
# it must be hit through the webserver directly.
DOCS_ROOT = os.path.join(dirs.PROJECT_DIR, 'docs/build')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!j^ld$kd&q+a$f*q5^o9i!yuxes1oe+l0x94bd6d)w8&8y4l2='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "clients.context_processors.klasses_cost",
    "main.context_processors.ignore_external_refs",
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'main.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'main.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(dirs.APP_DIR, 'templates'),
)

FIXTURE_DIRS = (
    # Be careful: when settings this folder, the initial_data file will be
    # loaded every time syncdb is called
    os.path.join(dirs.APP_DIR, 'fixtures'),
)

LOCALE_PATHS = (
    os.path.join(dirs.PROJECT_DIR, 'locale'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'south',
    'django_nose',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'lettuce.django',

    'django_localflavor_br',
    'utils',
    'accounts',
    'exercises',
    'clients',
    'excludeddates',
    'demonstrations',
    'followup',
    'payments',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Auth settings
AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
    'main.auth_backends.EmailBackend',
)
AUTH_PROFILE_MODULE = 'accounts.Profile'
LOGIN_URL = reverse_lazy('home')

# Grappelli settings
GRAPPELLI_ADMIN_TITLE = u'Mainiti'
GRAPPELLI_INDEX_DASHBOARD = 'main.dashboard.CustomIndexDashboard'

# Django nose default settings
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

LETTUCE_TEST_SERVER = 'lettuce.django.server.DjangoServer'
LETTUCE_SERVER_PORT = 7000
LETTUCE_USE_TEST_DATABASE = True
LETTUCE_APPS = (
    'demonstrations',
    'clients',
)


# Set this to True to make the templates ignore external references calls
# (like custom fonts or social branding). This is useful to speed up tests.
IGNORE_EXTERNAL_REFS = False

# wkhtmltopdf configurations
WKHTMLTOPDF_CMD = '/usr/local/bin/wkhtmltopdf'

WKHTMLTOPDF_CMD_OPTIONS = {
    'print-media-type': True,
    'quiet': True,
    'page-size': 'A4',
    'margin-top': '3.5cm',
    'margin-bottom': '1.5cm',
    'margin-left': '1.5cm',
    'margin-right': '1.5cm',
}

SPLINTER_TEST_DRIVER = 'phantomjs'

# default cost per class, can be customized if necessary
KLASSES_COST = Decimal(70)

# default day to generate payment, can be customized if necessary
PAYMENT_DAY = 15
MINIMAL_PAYMENT_COST = 20
LATE_PAYMENT = 5
