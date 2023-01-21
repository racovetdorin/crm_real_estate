from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField

from audit.models import AuditableModel
from clients.models import Client
from crm.models import SoftDeleteModel
from locations.models import Region, City, Zone
from offices.models import Office
from properties.models import Property, HotelAttributes, CommercialAttributes, LandAttributes, ApartmentAttributes, \
    HouseAttributes, StudioAttributes, CabinAttributes, GarageAttributes, BasementParkingAttributes, StorageRoomAttributes
from users.models import User


class Demand(AuditableModel, SoftDeleteModel):
    class Type(models.TextChoices):
        SALE = 'sale', _('Buy')
        RENT = 'rent', _('Rent')

    class ContractType(models.TextChoices):
        SMALL = 'small', '1.5%'
        MEDIUM = 'medium', '2.0%'
        BIG = 'big', '50%'

    class Status(models.TextChoices):
        INCOMPLETE = 'prospect', _('Prospect')
        ACTIVE = 'contracted', _('Contracted')
        TRANSACTED = 'transacted', _('Request transacted by us')
        TRANSACTED_BY_OTHERS = 'transacted_by_others', _('Request transacted by others')
        TRANSACTED_BY_OWNER = 'transacted_by_owner', _('Request transacted by owner')
        WITHDRAWN = 'withdrawn', _('Request withdrawn')

    class UnitsOfMeasure(models.TextChoices):
        SQUARE_METERS = 'square_meters', _('Square meters')
        ACRES = 'acres', _('Acres')
        HECTARES = 'hectares', _('Hectares')
    
    
    units_of_measure = models.CharField(max_length=50, blank=True, null=True, choices=UnitsOfMeasure.choices,
                                        default=UnitsOfMeasure.SQUARE_METERS,
                                        verbose_name=_('Units of measure'),
                                        )

    subtype_choices = HouseAttributes.Subtype.choices + ApartmentAttributes.Subtype.choices + \
                      StudioAttributes.Subtype.choices + CommercialAttributes.Subtype.choices + \
                      LandAttributes.Subtype.choices + CabinAttributes.Subtype.choices + \
                      HotelAttributes.Subtype.choices + GarageAttributes.Subtype.choices + \
                      BasementParkingAttributes.Subtype.choices + StorageRoomAttributes.Subtype.choices


    region = models.ForeignKey(Region, blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name=_(u'Region'))
    city = models.ForeignKey(City, blank=True, null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=_(u'City'))
    zones = models.ManyToManyField(Zone, blank=True,
                                   verbose_name=_(u'Zones'))

    user = models.ForeignKey(User, null=True, related_name="demands", on_delete=models.SET_NULL, blank=True,
                             verbose_name=_('Agent'))
    office = models.ForeignKey(Office, db_index=True, null=True, related_name="demands", on_delete=models.SET_NULL,
                               blank=True,
                               verbose_name=_('Office'))
    client = models.ForeignKey(Client, db_index=True, null=True, related_name="demands", on_delete=models.SET_NULL,
                               blank=True,
                               verbose_name=_('Client'))

    status = models.CharField(null=True, blank=True, max_length=50, choices=Status.choices, default=Status.INCOMPLETE,
                              verbose_name=_('Status'))
    type = models.CharField(max_length=56, blank=True, choices=Type.choices, verbose_name=_('Transaction type'))
    property_type = models.CharField(max_length=56, blank=True, choices=Property.Type.choices,
                                     verbose_name=_('Property type'))
    property_subtype = models.CharField(max_length=56, blank=True, choices=subtype_choices,
                                        verbose_name=_('Property subtype'))

    lead_source = models.ForeignKey('demands.LeadSource', blank=True, null=True,
                                    related_name='demands',
                                    on_delete=models.SET_NULL,
                                    verbose_name=_(u'Lead source'))
    final_price = models.IntegerField(null=True, blank=True, verbose_name=_(u'Final price'))
    commission = models.IntegerField(null=True, blank=True, verbose_name=_('Commission Seller'))
    commission_percent = models.FloatField(null=True, blank=True, verbose_name=_('Commission Seller %'))
    commission_buyer = models.IntegerField(null=True, blank=True, verbose_name=_('Commission Buyer'))
    commission_buyer_percent = models.FloatField(null=True, blank=True, verbose_name=_('Commission Buyer %'))
    commission_success = models.FloatField(null=True,
                                             blank=True, verbose_name=_(u'Commission for successful transaction'))
    commission_colaboration = models.FloatField(null=True,
                                           blank=True, verbose_name=_(u'Commission for colaboration'))
    country = CountryField( null=True, blank=True, blank_label=_('Demand Country'))

    features = models.ManyToManyField("properties.Feature", blank=True, verbose_name=_('Features'))
    top_floor_excluded = models.BooleanField(default=False, verbose_name=_('Top floor excluded'))
    ground_floor_excluded = models.BooleanField(default=False, verbose_name=_('Ground floor excluded'))
    mansard_excluded = models.BooleanField(default=False, verbose_name=_('Mansard excluded'))
    new_building = models.BooleanField(default=False, verbose_name=_('New building'))
    in_development = models.BooleanField(default=False, verbose_name=_('In development'))
    key_holding = models.BooleanField(default=False, verbose_name=_('Key holding'))
    active = models.BooleanField(default=True, verbose_name=_('Active'))

    contract_number = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Contract number'))
    contract_signing_date = models.DateTimeField(blank=True, null=True,
                                                 verbose_name=_('Contract signing date'))  # deprecated
    contract_register_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Contract register'))

    contract_start_date = models.DateField(null=True, blank=True, verbose_name=_('Contract signing date'))
    contract_type = models.CharField(max_length=70, null=True, blank=True, choices=ContractType.choices,
                                     verbose_name=_('Contract type'))

    price_min = models.IntegerField(null=True, blank=True, verbose_name=_('Price min'))
    price_max = models.IntegerField(null=True, blank=True, verbose_name=_('Price max'))

    surface_min = models.FloatField(null=True, blank=True, verbose_name=_('Surface min'))
    surface_max = models.FloatField(null=True, blank=True, verbose_name=_('Surface max'))

    rooms = MultiSelectField(max_length=50, null=True, blank=True,
                             choices=((x, str(x)) if x != 4 else (x, str(x) + ' +') for x in range(1, 5)),
                             verbose_name=_('Rooms'))

    limit_date = models.DateField(null=True, blank=True, verbose_name=_('Limit date'))
    comments = models.TextField(max_length=2000, null=True, blank=True, verbose_name=_('Comments'))
    offers_of_interest = models.ManyToManyField(Property, blank=True, verbose_name=_('Offers of interest'))

    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name=_('Updated At'))

    is_closed = models.BooleanField(default=False, verbose_name=_('Close Demand'))
    closing_date = models.DateField(null=True, blank=True, verbose_name=_('Closing date'))

    def __str__(self):
        return '{} {}'.format(self.id, _(self.get_display_object_class()))

    def get_absolute_url(self):
        return reverse(settings.DEMANDS_UPDATE_ROUTE, args=[self.id])

    def get_display_type(self):
        return self.Type(self.type).label if self.type else "Undefined"

    def get_display_property_type(self):
        return Property.Type(self.property_type).label if self.property_type else "Undefined"

    def get_display_price(self):
        return '{} - {}'.format(self.price_min, self.price_max)

    def get_display_object_class(self):
        return self.__class__.__name__

    def get_background_color(self):
        BLUE = '#B6DCDF'
        RED = '#FDCECE'

        if self.active:
            return BLUE

        return RED

    def get_zone_partial_text(self):
        zones = [str(zone) for zone in self.zones.all()]
        text = ' | '.join(zones)

        if len(text) > 25:
            text = text[:22] + '...'

        return text

    def get_full_zone_text(self):
        zones = [str(zone) for zone in self.zones.all()]
        return ' | '.join(zones)


class LeadSource(SoftDeleteModel):
    name = models.CharField(max_length=80, verbose_name=_(u'Source lead name'))
    slug = models.CharField(blank=True, max_length=80, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
