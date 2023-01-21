from django.conf import settings
from django.db.models import Q
from django.db.utils import ProgrammingError
from django.utils.translation import ugettext_lazy as _
import django_filters

from locations.models import Street, Zone, City
from offers.models import Offer
from properties.models import BaseConstructionAttributes, PROPERTY_SUBTYPE_CHOICES
from properties.models import Feature
from properties.models import Property
from properties.utils import get_property_attributes_filter_queryset
from users.models import User
from offices.models import Office


class PropertyFilter(django_filters.FilterSet):
    filtered_features = {}

    def __init__(self, *args, **kwargs):

        try:
            features = Feature.objects.filter(is_filtered=True)
        except ProgrammingError:
            pass
        else:
            for feature in features:
                filtered_feature_name = '_'.join(feature.name.lower().split())
                feature_filter = django_filters.CharFilter(label=_(feature.name), field_name='features')
                self.filtered_features[filtered_feature_name] = feature_filter
        super(PropertyFilter, self).__init__(*args, **kwargs)

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.filters['city'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.filters['zone'].field.choices = [(zone.pk, zone) for zone in
                                                      Zone.objects.filter(city_id=city_id).order_by('name')]

            except (ValueError, TypeError) as e:
                print(str(e))
                pass  # invalid input from the client; ignore and fallback to empty queryset

        if 'zone' in self.data:
            try:
                zones = [int(zone) for zone in self.data.getlist('zone')]
                self.filters['street'].queryset = Street.objects.filter(zone_id__in=zones).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset

    locals().update(filtered_features)

    user = django_filters.ModelChoiceFilter(queryset=User.objects.filter(is_active=True), method='user_filter')
    office = django_filters.ModelChoiceFilter(queryset=Office.objects.filter(is_active=True), method='office_filter')
    type = django_filters.MultipleChoiceFilter(choices=Property.Type.choices, label=_("Property type(s)"))
    subtype = django_filters.MultipleChoiceFilter(method='subtype_filter', choices=PROPERTY_SUBTYPE_CHOICES,
                                                  label=_("Property subtype(s)"))
    zone = django_filters.MultipleChoiceFilter(label=_("Zone"))

    client = django_filters.NumberFilter(method='client_filter', label=_('Client'))

    status = django_filters.ChoiceFilter(choices=settings.STATUS.choices,
                                         method='status_filter', label=_("Status"))
    offer_id = django_filters.NumberFilter(method='offer_id_filter', label=_('Offer ID'))
    price_min = django_filters.NumberFilter(method='price_filter_min', label=_("Price min"))
    price_max = django_filters.NumberFilter(method='price_filter_max', label=_("Price max"))
    surface_total_min = django_filters.NumberFilter(method='surface_total_filter_min', label=_("Minimum total surface"))
    surface_total_max = django_filters.NumberFilter(method='surface_total_filter_max', label=_("Maximum total surface"))
    surface_util_min = django_filters.NumberFilter(method='surface_util_filter_min', label=_("Minimum util surface"))
    surface_util_max = django_filters.NumberFilter(method='surface_util_filter_max', label=_("Maximum util surface"))
    created_at_min = django_filters.DateTimeFilter(method='created_at_filter_min', label=_("Created after"))
    created_at_max = django_filters.DateTimeFilter(method='created_at_filter_max', label=_("Created before"))
    sale_offers = django_filters.BooleanFilter(method='sale_offers_filter', label=_("Sale"))
    rent_offers = django_filters.BooleanFilter(method='rent_offers_filter', label=_("Rent"))
    built = django_filters.ChoiceFilter(method='built_filter', label=_("Built"),
                                        choices=settings.BUILT_PERIOD.choices)
    comfort = django_filters.ChoiceFilter(choices=BaseConstructionAttributes.Comfort.choices,
                                          method='comfort_filter', label=_("Comfort"))
    partitioning = django_filters.ChoiceFilter(choices=BaseConstructionAttributes.Partitioning.choices,
                                               method='partitioning_filter', label=_("Partitioning"))
    interior_state = django_filters.ChoiceFilter(choices=settings.INTERIOR_STATE.choices,
                                                 method='interior_state_filter', label=_("Interior state"))
    energy_class = django_filters.ChoiceFilter(choices=BaseConstructionAttributes.EnergyEfficiency.choices,
                                               method='energy_class_filter', label=_('Energy class'))
    heating_source = django_filters.ChoiceFilter(choices=BaseConstructionAttributes.HeatingSource.choices,
                                                 method='heating_source_filter', label=_('Heating source'))
    rooms_number = django_filters.MultipleChoiceFilter(method='rooms_number_filter',
                                                       choices=[(x, str(x)) if x != 4 else (x, '+' + str(x)) for x in
                                                                range(1, 5)],
                                                       label='Rooms filter')

    bathrooms_number = django_filters.MultipleChoiceFilter(method='bathrooms_number_filter',
                                                           choices=[(x, str(x)) if x != 3 else (x, '+' + str(x)) for x
                                                                    in
                                                                    range(1, 4)],
                                                           label='Bathrooms filter')

    garage = django_filters.ChoiceFilter(method='garage_filter', choices=BaseConstructionAttributes.GarageType.choices,
                                         label=_('Garage'))
    furnished = django_filters.ChoiceFilter(method='furnished_filter',
                                            choices=BaseConstructionAttributes.Furnished.choices, label=_('Furnished'))
    windows = django_filters.ChoiceFilter(method='windows_filter',
                                          choices=BaseConstructionAttributes.WindowsType.choices, label=_('Windows'))
    internet_connection = django_filters.ChoiceFilter(method='internet_filter',
                                                      choices=BaseConstructionAttributes.InternetConnection.choices,
                                                      label=_('Internet'))

    recommended = django_filters.BooleanFilter(method='recommended_filter', label=_('Recommended'))
    exclusive = django_filters.BooleanFilter(method='exclusive_filter', label=_('Exclusive'))
    key_holding = django_filters.BooleanFilter(method='key_holding_filter', label=_('Key Holding'))
    homepage = django_filters.BooleanFilter(method='homepage_filter', label=_('Homepage'))

    class Meta:
        model = Property
        fields = ['id', 'region', 'city', 'zone', 'street', 'offers', 'features']

    def user_filter(self, queryset, name, value):
        return queryset.filter(user=value)

    def office_filter(self, queryset, name, value):
        return queryset.filter(office=value)

    def subtype_filter(self, queryset, name, value):
        qs = None
        for v in value:
            filter = get_property_attributes_filter_queryset('subtype', v)

            if not qs:
                qs = Q(filter)
            else:
                qs |= Q(filter)

        return queryset.filter(qs)

    def client_filter(self, queryset, name, value):
        return queryset.filter(client=value)

    def status_filter(self, queryset, name, value):
        return queryset.filter(offers__status=value, offers__is_closed=False)

    def recommended_filter(self, queryset, name, value):
        return queryset.filter(offers__is_recommended=value)

    def exclusive_filter(self, queryset, name, value):
        return queryset.filter(offers__exclusive=value)

    def key_holding_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('key_holding', value))

    def homepage_filter(self, queryset, name, value):
        return queryset.filter(offers__homepage=value)

    def offer_id_filter(self, queryset, name, value):
        return queryset.filter(offers__id=value)

    def price_filter_min(self, queryset, name, value):
        return queryset.filter(offers__price__gte=value)

    def price_filter_max(self, queryset, name, value):
        if value == 500_000:
            return queryset.filter(offers__price__gte=value)

        return queryset.filter(offers__price__lte=value)

    def surface_total_filter_min(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('surface_total__gte', value))

    def surface_total_filter_max(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('surface_total__lte', value))

    def surface_util_filter_min(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('surface_util__gte', value))

    def surface_util_filter_max(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('surface_util__lte', value))

    def built_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('built', value))

    def comfort_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('comfort', value))

    def partitioning_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('partitioning', value))

    def interior_state_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('interior_state', value))

    def energy_class_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('energy_class', value))

    def heating_source_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('heating_source', value))

    def garage_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('garage', value))

    def rooms_number_filter(self, queryset, name, value):
        qs = None
        for v in value:
            filter = get_property_attributes_filter_queryset('rooms_number', v)
            if not int(v) <= 3:
                filter = get_property_attributes_filter_queryset('rooms_number__gte', 4)

            if not qs:
                qs = Q(filter)
            else:
                qs |= Q(filter)

        return queryset.filter(qs)

    def bathrooms_number_filter(self, queryset, name, value):
        qs = None
        for v in value:
            filter = get_property_attributes_filter_queryset('bathrooms_number', v)
            if not int(v) <= 2:
                filter = get_property_attributes_filter_queryset('bathrooms_number__gte', 3)

            if not qs:
                qs = Q(filter)
            else:
                qs |= Q(filter)

        return queryset.filter(qs)

    def created_at_filter_min(self, queryset, name, value):
        return queryset.filter(created_at__gte=value)

    def created_at_filter_max(self, queryset, name, value):
        return queryset.filter(created_at__lte=value)

    def sale_offers_filter(self, queryset, name, value):
        return queryset.filter(offers__type=Offer.ContractType.SALE)

    def rent_offers_filter(self, queryset, name, value):
        return queryset.filter(offers__type=Offer.ContractType.RENT)
