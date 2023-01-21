import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from locations.models import City
from crm.models import SoftDeleteModel, ImageModel


class Office(SoftDeleteModel):
    name = models.CharField(max_length=50, blank=True, verbose_name=_('Name'))
    email = models.EmailField(max_length=256, blank=True, null=True, verbose_name=_('Email'))
    phone_1 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone 1'))
    phone_2 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone 2'))
    phone_3 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone 3'))
    slug = models.CharField(max_length=50, blank=True, unique=True, verbose_name=_('Slug'))
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Address'))
    show_on_site = models.BooleanField(default=False, verbose_name=_('Show on site'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is active'))
    external_id = models.CharField(max_length=50, default=uuid.uuid4, verbose_name=_(u'Office external ID'))
    latitude = models.FloatField(blank=True, null=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_('Longitude'))
    postal_code = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Postal code'))
    international_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('International ID'))
    city_gobal_id = models.ForeignKey(City, db_index=True, null=True,
                                      blank=True, on_delete=models.SET_NULL, related_name='city',
                                      verbose_name=_('Rex ID City'))
    office_url = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Web Office URL'))
    office_image_url = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Office Image URL'))
    office_description = models.TextField(max_length=2000, blank=True, null=True, verbose_name=_('Office Description'))
    order = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Office order'))

    def save(self, *args, **kwargs):
        # if slugify(self.name) != self.slug: # we need to can modify office slug as we want in admin
            # self.slug = slugify(self.name)
        super(Office, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(settings.OFFICES_UPDATE_ROUTE, args=[self.id])

    def get_thumbnail_url(self):
        try:
            return self.images.filter(office_id=self.id).order_by('position').first().image_path
        except AttributeError:
            return None

    def get_display_object_class(self):
        return self.__class__.__name__


class OfficeImage(ImageModel):
    office = models.ForeignKey(Office, related_name="images", on_delete=models.CASCADE,
                               verbose_name=_('Office'), blank=True, null=True)

    def __str__(self):
        return 'Image for office with id: {}'.format(self.office.pk)
