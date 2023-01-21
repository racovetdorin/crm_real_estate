from .settings import *


DEBUG = True


def show_toolbar(request):
    return DEBUG


GEO_COORDINATES_DEFAULT = 46.769349043202965, 23.58974706867647

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

# Application definition

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
