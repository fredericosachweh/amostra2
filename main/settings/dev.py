try:
    from custom import INSTALLED_APPS
except ImportError:
    from base import INSTALLED_APPS
try:
    from custom import MIDDLEWARE_CLASSES
except ImportError:
    from base import MIDDLEWARE_CLASSES


INSTALLED_APPS = INSTALLED_APPS + (
    'django_extensions',
    'debug_toolbar'
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# debug-toolbar-config can be replaces in the custom settings
try:
    DEBUG_TOOLBAR_CONFIG
except NameError:
    DEBUG_TOOLBAR_CONFIG = {
        'ENABLE_STACKTRACES' : True,
    }
