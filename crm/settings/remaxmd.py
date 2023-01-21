from .settings import *
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import global_settings

DEBUG = True

CDN_MEDIA_URL = config('CDN_MEDIA_URL')

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = False

GEO_COORDINATES_DEFAULT = 47.02472305395979, 28.83250530104991

import django.conf.locale

USE_I18N = True
USE_L10N = True


LANGUAGE_CODE = 'ro'
LANGUAGES = (
    ('ro', _('Romanian')),
    ('md', _('Romanian')),
    ('en', _('English'))
)
EXTRA_LANG_INFO = {
    'md': {
        'bidi': False,
        'code': 'md',
        'name': 'Romanian',
        'name_local': _('Romanian'),
    },
}

# LANG_INFO = {**django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO}
# django.conf.locale.LANG_INFO = LANG_INFO
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO
global_settings.LANGUAGES = global_settings.LANGUAGES + [("md", 'Romanian')]


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'ui/locale').replace('\\', '/')
]


TRANSACTED_OFFERS_LOG_FIELDS = OrderedDict([
    ('user_name', _(u'Agent name')),
    ('office_name', _(u'Office name')),
    ('id', _(u'Transacted offer ID')),
    ('exclusive', _(u'Exclusivity')),
    ('type', _(u'Type')),
    ('final_price', _(u'Price')),
    ('commission_percent', _(u'Commission %')),
    ('commission', _(u'Commission')),
    ('closing_date', _(u'Offer closing date')),
    ('user_email', _(u'Agent email')),
    ('user_id', _(u'Agent ID')),
    ('office_id', _(u'Office ID')),
    ('created_at', _(u'Created at')),
    ('updated_at', _(u'Updated at')),
])

CRM_TUTORIALS = (
    ('Adăugare Proprietate', 'https://media-remaxmd.fra1.digitaloceanspaces.com/tutorials/AdaugareProprietate'),
)


STORAGE_DNS = config('STORAGE_DNS')
IMG_PROXY_KEY = config('IMG_PROXY_KEY')
IMG_PROXY_SALT = config('IMG_PROXY_SALT')
IMG_PROXY_HOST = config('IMG_PROXY_HOST')
IMG_PROXY_HOST_999 = 'https://thumbs999.rmx.casa'

class ConstructionMaterials(models.TextChoices):
    BRICK = 'brick', _('Brick')
    CONCRETE = 'concrete', _('Concrete')
    BCA = 'bca', _('BCA')
    WOOD = 'wood', _('Wood')
    LIMESTONE = 'limestone', _('Limestone')


class BuiltPeriod(models.TextChoices):
    BEFORE_1960 = 'before_1960', _('Before 1960')
    BETWEEN_1960_2010 = 'between_1960_2010', _('Between 1960 - 2010')
    AFTER_2010 = 'after_2010', _('After 2010')


class InteriorState(models.TextChoices):
    IN_WHITE = 'in white', _('In white')
    IN_GREY = 'in grey', _('In grey')
    WITH_FIXES = 'with fixes', _('With fixes')
    UNFINISHED = 'unfinished', _('Unfinished')
    LUX = 'lux', _('Luxurious')


class Status(models.TextChoices):
    INCOMPLETE = 'incomplete', _('Incomplete')
    PENDING = 'pending', _('Pending')
    ACTIVE = 'active', _('Active')
    RESERVED = 'reserved', _('Reserved')
    TRANSACTED = 'transacted', _('Transacted by us')
    TRANSACTED_BY_OTHERS = 'transacted_by_others', _('Transacted by others')
    TRANSACTED_BY_OWNER = 'transacted_by_owner', _('Transacted by owner')
    WITHDRAWN = 'withdrawn', _('Withdrawn')


class ROLES(models.TextChoices):
    COUNSELOR = 'counselor', _('Real estate counselor')
    MANAGING_DIRECTOR = 'managing_director', _('Managing director')
    ASSISTANT_MANAGER = 'assistant_manager', _('Assistant manager')
    SECRETARIAT = 'secretariat', _('Secretariat')
    IT_ADMINISTRATOR = 'it_administrator', _('IT Administrator')
    SPECIALIST = 'specialist', _('Real estate specialist')
    BROKER_OWNER = 'broker_owner', _('Broker owner')
    MARKETING_MANAGER = 'marketing_manager', _('Marketing Manager')
    MORTAGE_BROKER = 'mortage_broker', _('Mortage Broker')
    OFFICE_MANAGER = 'office_manager', _('Office Manager')


CONSTRUCTION_MATERIALS = ConstructionMaterials
BUILT_PERIOD = BuiltPeriod
INTERIOR_STATE = InteriorState
STATUS = Status

STATUS_CHOICES_1 = (
    (STATUS.PENDING.value, STATUS.PENDING.label),
    (STATUS.INCOMPLETE.value, STATUS.INCOMPLETE.label),
)

STATUS_CHOICES_2 = (
    (STATUS.ACTIVE.value, STATUS.ACTIVE.label),
    (STATUS.RESERVED.value, STATUS.RESERVED.label),
    (STATUS.TRANSACTED.value, STATUS.TRANSACTED.label),
    (STATUS.TRANSACTED_BY_OTHERS.value, STATUS.TRANSACTED_BY_OTHERS.label),
    (STATUS.TRANSACTED_BY_OWNER.value, STATUS.TRANSACTED_BY_OWNER.label),
)

STATUS_CHOICES_3 = (
    (STATUS.TRANSACTED.value, STATUS.TRANSACTED.label),
    (STATUS.TRANSACTED_BY_OTHERS.value, STATUS.TRANSACTED_BY_OTHERS.label),
    (STATUS.TRANSACTED_BY_OWNER.value, STATUS.TRANSACTED_BY_OWNER.label),
    (STATUS.WITHDRAWN.value, STATUS.WITHDRAWN.label),
)

STATUS_CONFIG = {
    Status.INCOMPLETE: STATUS_CHOICES_1,
    Status.PENDING: STATUS_CHOICES_1,
    Status.ACTIVE: STATUS_CHOICES_2,
    Status.RESERVED: STATUS_CHOICES_2,
    Status.TRANSACTED: ((Status.TRANSACTED.value, Status.TRANSACTED.label),),
    Status.TRANSACTED_BY_OTHERS: ((Status.TRANSACTED_BY_OTHERS.value, Status.TRANSACTED_BY_OTHERS.label),),
    Status.TRANSACTED_BY_OWNER: ((Status.TRANSACTED_BY_OWNER.value, Status.TRANSACTED_BY_OWNER.label),),
    Status.WITHDRAWN: ((Status.WITHDRAWN.value, Status.WITHDRAWN.label),)
}

TRANSACTED_STATUSES_CHOICES = (
    ('', '----------'),
    (STATUS.TRANSACTED.value, STATUS.TRANSACTED.label),
    (STATUS.TRANSACTED_BY_OTHERS.value, STATUS.TRANSACTED_BY_OTHERS.label),
    (STATUS.TRANSACTED_BY_OWNER.value, STATUS.TRANSACTED_BY_OWNER.label),
)

OFFER_CREATION_STATUS_CHOICES = STATUS_CHOICES_1

CLIENT = 'rmm'
