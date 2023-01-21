
from .settings import *

from .settings import CONSTRUCTION_MATERIALS
from .settings import BUILT_PERIOD
from .settings import INTERIOR_STATE
from .settings import STATUS
from .settings import COMMISSION_CHOICES

DEBUG = True

CDN_MEDIA_URL = config('CDN_MEDIA_URL')

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = False
