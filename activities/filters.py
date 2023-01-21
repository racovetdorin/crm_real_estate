import django_filters
from django.conf import settings
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

from activities.models import Activity


class ActivityFilter(django_filters.FilterSet):
    due_date_min = django_filters.DateTimeFilter(method='due_date_filter_min', label=_("Due Date Min"),
                                                 widget=TextInput(attrs={'placeholder': settings.DATE_FORMAT_RO}))
    due_date_max = django_filters.DateTimeFilter(method='due_date_filter_max', label=_("Due Date Max"),
                                                 widget=TextInput(attrs={'placeholder': settings.DATE_FORMAT_RO}))
    created_at_min = django_filters.DateTimeFilter(method='created_at_filter_min', label=_("Created At Min"),
                                                   widget=TextInput(attrs={'placeholder': settings.DATE_FORMAT_RO}))
    created_at_max = django_filters.DateTimeFilter(method='created_at_filter_max', label=_("Created At Max"),
                                                   widget=TextInput(attrs={'placeholder': settings.DATE_FORMAT_RO}))
    is_taken = django_filters.BooleanFilter(method='is_taken_filter', label=_('Not Taken'))

    title = django_filters.CharFilter(label=_('Title'), lookup_expr='icontains')

    phone = django_filters.CharFilter(label=_('Phone'), lookup_expr='icontains')

    property = django_filters.NumberFilter(method='property_filter', label=_('Property'))

    demand = django_filters.NumberFilter(method='demand_filter', label=_('ID Demand'))

    client = django_filters.NumberFilter(method='client_filter', label=_('Client'))

    id = django_filters.NumberFilter(field_name='id', label=_('ID Activity'))

    class Meta:
        model = Activity
        fields = ['status', 'id', 'type', 'title', 'phone', 'description', 'due_date', 'priority', 'user', 'created_at',
                  'is_taken', 'demand']

    def due_date_filter_min(self, queryset, name, value):
        return queryset.filter(due_date__gte=value)

    def due_date_filter_max(self, queryset, name, value):
        return queryset.filter(due_date__lte=value)

    def created_at_filter_min(self, queryset, name, value):
        return queryset.filter(created_at__gte=value)

    def created_at_filter_max(self, queryset, name, value):
        return queryset.filter(created_at__lte=value)

    def is_taken_filter(self, queryset, name, value):
        return queryset.exclude(is_taken=value)

    def property_filter(self, queryset, name, value):
        return queryset.filter(property=value)

    def demand_filter(self, queryset, name, value):
        return queryset.filter(demand=value)

    def client_filter(self, queryset, name, value):
        return queryset.filter(client=value)
