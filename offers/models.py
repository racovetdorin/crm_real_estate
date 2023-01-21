import datetime

from builtins import property as builtin_property
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from audit.models import ModelDiffMixin
from clients.models import Client
from crm.models import SoftDeleteModel
from django.conf import settings
from offices.models import Office
from users.models import User


class Offer(ModelDiffMixin, SoftDeleteModel):
    class ContractType(models.TextChoices):
        SALE = 'sale', _('Sale')
        RENT = 'rent', _('Rent')

    class WithdrawnReason(models.TextChoices):
        EXPIRED_CONTRACT = 'expired_contract', _('Expired contract')
        CANCELLED_CONTRACT = 'cancelled_contract', _('Cancelled contract')
        OTHER = 'other', _('Other')

    class VATChoices(models.TextChoices):
        INCLUDED = 'included', _('VAT Included')
        PLUS_VAT = 'plus_vat', _('Plus VAT')

    user = models.ForeignKey(User, db_index=True, null=True, related_name='offers', on_delete=models.SET_NULL,
                             verbose_name=_('Agent'))
    office = models.ForeignKey(Office, db_index=True, null=True, related_name="offers", on_delete=models.SET_NULL,
                               verbose_name=_('Office'))

    status = models.CharField(null=True, blank=True, max_length=50, choices=settings.STATUS.choices,
                              default=settings.STATUS.INCOMPLETE,
                              verbose_name=_('Status'))

    withdrawn_reason = models.CharField(null=True, blank=True, max_length=50, choices=WithdrawnReason.choices,
                                        verbose_name=_('Withdrawn reason'))

    type = models.CharField(null=True, blank=True, max_length=56, choices=ContractType.choices,
                            default=ContractType.SALE, verbose_name=_('Type'))

    property = models.ForeignKey('properties.Property', null=True, related_name="offers", on_delete=models.SET_NULL,
                                 verbose_name=_('Property'))

    promote_site = models.BooleanField(default=False, verbose_name=_('Promote site'))
    promote_site_homepage = models.BooleanField(default=False, verbose_name=_('Promote site homepage'))
    promoted = models.BooleanField(default=False, verbose_name=_('Promoted'))

    price = models.IntegerField(null=True, blank=True, verbose_name=_('Offer price'))
    price_old = models.IntegerField(null=True, blank=True, verbose_name=_('Old price'))
    price_hot = models.BooleanField(null=False, default=False, verbose_name=_('Hot price'))
    price_minimum = models.IntegerField(null=True, blank=True, verbose_name=_('Price minimum'))
    price_per_sqm = models.IntegerField(null=True, blank=True, verbose_name=_('Price per m2'))

    exclusive = models.BooleanField(null=False, default=False, verbose_name=_('Exclusive'))
    special_offer = models.BooleanField(null=False, default=False,
                                        verbose_name=_('Special offer'))  # Deprecated - should not be used
    is_recommended = models.BooleanField(null=False, default=False, verbose_name=_('Recommended'))
    homepage = models.BooleanField(null=False, default=False,
                                   verbose_name=_('Homepage'))  # Deprecated - should not be used

    contract_number = models.CharField(max_length=256, blank=True, null=True, default='',
                                       verbose_name=_('Contract number'))
    contract_signing_date = models.DateTimeField(blank=True, null=True,
                                                 verbose_name=_('Contract register'))  # deprecated
    contract_register_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Contract register'))

    contract_start_date = models.DateField(null=True, blank=True, verbose_name=_('Contract signing date'))
    contract_end_date = models.DateField(null=True, blank=True, verbose_name=_('Contract end date'))

    final_price = models.IntegerField(null=True, blank=True, verbose_name=_(u'Final price'))
    commission = models.IntegerField(null=True, blank=True, verbose_name=_('Commission Seller'))
    commission_buyer = models.IntegerField(null=True, blank=True, verbose_name=_('Commission Buyer'))
    commission_buyer_percent = models.FloatField(null=True, blank=True, verbose_name=_('Commission Buyer %'))
    commission_success = models.FloatField(null=True,
                                             blank=True, verbose_name=_(u'Commission for successful transaction'))
    commission_colaboration = models.FloatField(null=True,
                                           blank=True, verbose_name=_(u'Commission for colaboration'))
    commission_percent = models.FloatField(null=True, blank=True, verbose_name=_('Commission Seller %'))
    buyer = models.ForeignKey(Client, blank=True, null=True, verbose_name=_(u'Buyer'), on_delete=models.SET_NULL)
    VAT = models.CharField(blank=True, max_length=56, choices=VATChoices.choices, default='', verbose_name=_('VAT'))

    is_closed = models.BooleanField(default=False, verbose_name=_('Close offer'))
    closing_date = models.DateField(null=True, blank=True, verbose_name=_('Closing date'))
    closed_by = models.CharField(max_length=256, default='', blank=True, verbose_name=_('Closed by'))

    view_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=_('View Count'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    is_validated = models.BooleanField(default=False, verbose_name=_('Validated'))
    validation_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Validation_date'))

    external_id = models.CharField(max_length=50, default=uuid.uuid4, verbose_name=_(u'Offer external ID'))

    mls_999 = models.BooleanField(default=False, verbose_name=_('999.MD')) # mls_promotion
    mls_999_data = models.JSONField(default=dict,blank=True, null=True)
    mls_remax_global = models.BooleanField(default=False, verbose_name=_('RE/MAX Global'))
    mls_remax_global_data = models.JSONField(default=dict,blank=True, null=True)

    advert_id_999 = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=_(u'Advert id 999'))
    casahub = models.BooleanField(default=False, verbose_name=_('Casahub.md')) # casahub promote
    makler = models.BooleanField(default=False, verbose_name=_('Makler.md')) # makler promote


    def __str__(self):
        return 'Offer ({})'.format(self.id)

    def get_display_status(self):
        return self.Status(self.status).label

    def get_display_object_class(self):
        return self.__class__.__name__

    @builtin_property
    def display_title(self):
        transaction = "vânzare" if self.type == self.ContractType.SALE else "închiriat"

        title = f"{self.property.attributes_object.get_title_prefix()} de {transaction}"

        return title

    def website_link(self):
        return f"https://remax.md/oferta/{self.id}"


class Notification(SoftDeleteModel):
    offer = models.ForeignKey(Offer, verbose_name=_('Offer'), on_delete=models.SET_NULL, related_name='notifications',
                              null=True, blank=True)
    title = models.CharField(max_length=256, verbose_name=_('Title'), default='', blank=True)
    is_viewed = models.BooleanField(default=False, verbose_name=_('Is viewed'))

