import requests
import rollbar
import django_rq 

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from locations.models import Country
from locations.models import Region
from locations.models import City
from locations.models import Zone
from locations.models import Street
from locations.models import StreetNumber
from locations.streets import get_all_street


from django.contrib import messages


class Citiesfilter(admin.SimpleListFilter):
    title = _('City')
    parameter_name = 'city_id'

    def lookups(self, request, model_admin):
        cities = City.objects.all()
        return [(city.id, city.display_name_admin) for city in cities]

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            return queryset.filter(city__id = int(self.value()))
        return queryset


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'type')
    list_filter = ('region', 'type')


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = (Citiesfilter, )
    raw_id_fields = ['city']


class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'region_name', 'city', 'zone', 'id_999', 'latitude', 'longitude')
    list_filter = (Citiesfilter, )
    raw_id_fields = ['city', 'zone']
    actions = ['add_streets']

    def add_streets(self, request, queryset):
        get_all_street()
        self.message_user(request, "Starting import of streets from 999 API ...", messages.SUCCESS)
    add_streets.short_description="Add 999 streets and street numbers"

    def region_name(self, obj):
        if obj.city and obj.city.region:
            return obj.city.region.name
        else:
            return ''

class StreetNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'street_name', 'region_name','city_name', 'latitude', 'longitude')

    def street_name(self, obj):
        return obj.street.name

    def city_name(self, obj):
        if obj.street.city:
            return obj.street.city.name
        else:
            return ''

    def region_name(self, obj):
        if obj.street.city.region:
            return obj.street.city.region.name
        else:
            return ''

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City, CityAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(StreetNumber, StreetNumberAdmin)