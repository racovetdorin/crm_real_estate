from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=256, blank=True)
    code = models.CharField(blank=True, max_length=10,
                            help_text=_(u"Country code (two characters) in ISO 3166-1 format"))

    class Meta:
        verbose_name = _(u'Country')
        verbose_name_plural = _(u'Countries')
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=256, blank=True)
    country = models.ForeignKey(Country, blank=True, null=True, related_name='regions', on_delete=models.SET_NULL)
    rex_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Rex Region ID'))
    id_999 = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Region ID 999'))
    class Meta:
        verbose_name = _(u'Region')
        verbose_name_plural = _(u'Regions')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_cities(self, type=None):
        cities = self.cities.all()
        if type:
            cities = cities.filter(type=type)
        return cities


class City(models.Model):
    class Type(models.TextChoices):
        CITY = 'city', _('City')
        COMMUNE = 'commune', _('Commune')
        VILLAGE = 'village', _('Village')

    name = models.CharField(max_length=256, blank=True)
    region = models.ForeignKey(Region, null=True, blank=True, related_name='cities', on_delete=models.SET_NULL)
    type = models.CharField(max_length=50, db_index=True, choices=Type.choices, blank=True)
    rex_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Rex City ID'))
    id_999 = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'City ID 999'))
    class Meta:
        verbose_name = _(u'City')
        verbose_name_plural = _(u'Cities')
        ordering = ['name']

    def display_name_admin(self):
        if self.region is not None:
            return f"{self.name} ({self.region.name})"
        else:
            return f"{self.name}"

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=256, blank=True)
    city = models.ForeignKey(City, null=True, blank=True, related_name='zones', on_delete=models.SET_NULL)
    rex_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Rex Zone ID'))
    id_999 = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Zone ID 999'))
    class Meta:
        verbose_name = _(u'Zone')
        verbose_name_plural = _(u'Zones')

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=256, verbose_name=_(u'Name'), blank=True)
    city = models.ForeignKey(City, blank=True, null=True, verbose_name=_(u'City'), related_name='streets',
                             on_delete=models.SET_NULL)
    zone = models.ForeignKey(Zone, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_(u'Zone'))
    id_999 = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Street ID 999'))
    latitude = models.FloatField(blank=True, null=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_('Longitude'))

    class Meta:
        verbose_name = _(u'Street')
        verbose_name_plural = _(u'Streets')

    def __str__(self):
        return self.name 


class StreetNumber(models.Model):
    number = models.CharField(max_length=50, verbose_name=_(u'Street Number'), blank=True)
    street = models.ForeignKey(Street, blank=True, null=True, verbose_name=_(u'Street'), related_name='number',
                             on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_('Longitude'))

    class Meta:
        verbose_name = _(u'Street Number')
        verbose_name_plural = _(u'Street Numbers')
    def __str__(self):
        return f"Numarul  {self.number}  , strada  {self.street}" 