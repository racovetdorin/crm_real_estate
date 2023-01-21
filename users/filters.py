import django_filters
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.utils.translation import ugettext_lazy as _

from users.models import User


class UserFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method='full_name_filter', label=_('Name'))
    email = django_filters.CharFilter(lookup_expr='icontains', label=_('Email'))
    phone = django_filters.NumberFilter(lookup_expr='icontains', label=_('Phone'))

    class Meta:
        model = User
        fields = ['email', 'role', 'id', 'phone', 'is_active']

    def full_name_filter(self, queryset, name, value):
        qs = queryset.annotate(full_name=Concat('first_name', V(' '), 'last_name'))

        qs = qs.filter(full_name__icontains=value)
        return qs
