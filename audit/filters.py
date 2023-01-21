import django_filters
from django.utils.translation import ugettext_lazy as _

from audit.models import AuditLog


class AuditLogFilter(django_filters.FilterSet):
    created_at_min = django_filters.DateTimeFilter(method='created_at_filter_min', label=_("Created After"))
    created_at_max = django_filters.DateTimeFilter(method='created_at_filter_max', label=_("Created Before"))
    id = django_filters.NumberFilter(method='id_filter', label=_('ID'))

    class Meta:
        model = AuditLog
        fields = ['created_at', 'user', 'object_type']

    def id_filter(self, queryset, name, value):
        return queryset.filter(object_id=value)
