import django_filters
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django.utils.translation import ugettext_lazy as _

from users.models import User
from clients.models import Client

class ClientFilter(django_filters.FilterSet):
    
    TYPES = {
        ('is_buyer', _('Buyer')),
        ('is_owner', _('Owner')),
    }

    full_name = django_filters.CharFilter(method='filter_case_insensitive', label=_("Name"))
    email = django_filters.CharFilter(method='filter_email', label="Email")
    all_phones = django_filters.NumberFilter(method='filter_phones', label=_("Phone"))
    all_agents = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                                  method="filter_agents", label=_("Agents"))
    
    
    type = django_filters.ChoiceFilter(label=_('Type'), choices=TYPES, method="filter_by_type")

    def __init__(self, user, *args, **kwargs):
        super(ClientFilter, self).__init__(*args, **kwargs)
        self.filters['all_agents'].queryset = User.objects.filter(office=user.office)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_1', 'phone_2', 'phone_3', 'is_agency', 'id']

    def filter_by_type(self, queryset, name, value):
        filters = filters = Q(is_buyer=True) if value == 'is_buyer' else Q(is_owner=True)
        qs = queryset.filter(filters)
        
        return qs
        

    def filter_agents(self, queryset, name, value):
        
        qs = queryset.filter(user_id=value)
        return qs

    def filter_case_insensitive(self, queryset, name, value):
        qs = queryset.annotate(full_name=Concat('first_name', V(' '), 'last_name'))
        qs = qs.filter(full_name__icontains=value)
        return qs

    def filter_email(self, queryset, name, value):
        return queryset.filter(email__icontains=value)

    def filter_phones(self, queryset, name, value):
        qs = queryset.annotate(all_phones=Concat('phone_1', V(' '), 'phone_2', V(' '), 'phone_3'))
        
        for phone in str(value).split(' '):
            qs = qs.filter(all_phones__icontains=phone)
        return qs
