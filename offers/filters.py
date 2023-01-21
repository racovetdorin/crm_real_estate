import django_filters
from django.utils.translation import ugettext_lazy as _

from offers.models import Offer
from users.models import User


class TransactedOffersFilter(django_filters.FilterSet):
    closed_after_date = django_filters.DateFilter(method='closed_after', label=_('Closed after date'))
    closed_before_date = django_filters.DateFilter(method='closed_before', label=_('Closed before date'))
    user_active = django_filters.ModelChoiceFilter(queryset=User.objects.filter(is_active=True), method='user_filter',
                                                   label=_("Active Agents"))

    class Meta:
        model = Offer
        fields = ['office', 'type', 'status']

    def user_filter(self, queryset, name, value):
        return queryset.filter(user=value)
    def closed_after(self, queryset, name, value):
        return queryset.filter(closing_date__gte=value)

    def closed_before(self, queryset, name, value):
        return queryset.filter(closing_date__lte=value)
