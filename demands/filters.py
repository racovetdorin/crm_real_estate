import django_filters
from django.utils.translation import ugettext_lazy as _

from demands.models import Demand
from users.models import User

class DemandFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(method='price_filter_min', label=_('Price Min'))
    price_max = django_filters.NumberFilter(method='price_filter_max', label=_('Price Max'))
    surface_min = django_filters.NumberFilter(method='surface_filter_min', label=_('Surface Min'))
    surface_max = django_filters.NumberFilter(method='surface_filter_max', label=_('Surface Max'))
    rooms_min = django_filters.NumberFilter(method='rooms_filter_min', label=_('Rooms Min'))
    rooms_max = django_filters.NumberFilter(method='rooms_filter_max', label=_('Rooms Max'))
    client = django_filters.NumberFilter(method='client_id_filter', label=_('Client ID'))
    user = django_filters.ModelChoiceFilter(queryset=User.objects.filter(is_active=True), method='user_filter')
    class Meta:
        model = Demand
        fields = [
            'id', 'active', 'type', 'region', 'city', 'property_type', 'property_subtype', 'lead_source', 
        ]

    def price_filter_min(self, queryset, name, value):
        return queryset.filter(price_min__gte=value)

    def price_filter_max(self, queryset, name, value):
        return queryset.filter(price_max__lte=value)

    def surface_filter_min(self, queryset, name, value):
        return queryset.filter(surface_min__gte=value)

    def surface_filter_max(self, queryset, name, value):
        return queryset.filter(surface_max__lte=value)

    def rooms_filter_min(self, queryset, name, value):
        return queryset.filter(surface_max__lte=value)

    def rooms_filter_max(self, queryset, name, value):
        return queryset.filter(surface_max__lte=value)

    def client_id_filter(self, queryset, name, value):
        return queryset.filter(client__id=value)

    def user_filter(self, queryset, name, value):
        return queryset.filter(user=value)
