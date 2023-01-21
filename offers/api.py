import datetime
from django.conf import settings
from django.db.models import Q
from django.db.utils import ProgrammingError
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from crm.api import BaseListAPIView, BaseRetrieveAPIView
from locations.models import Zone
from offers.models import Offer
from offers.serializers import OfferDetailsSerializer
from offers.serializers import OfferListSerializer
from properties.models import ApartmentAttributes, BaseConstructionAttributes, CommercialAttributes, HouseAttributes
from properties.models import Feature
from properties.models import Property
from properties.utils import get_property_attributes_filter_queryset



class OffersAPIFilters(filters.FilterSet):
    filtered_features = {}
    property_type_value = ""

    def __init__(self, *args, **kwargs):

        try:
            features = Feature.objects.filter(is_filtered=True)
        except ProgrammingError:
            pass
        else:
            for feature in features:
                filtered_feature_name = '_'.join(feature.name.lower().split())
                feature_filter = filters.CharFilter(label=_(feature.name), field_name='property__features')
                self.filtered_features[filtered_feature_name] = feature_filter

        super(OffersAPIFilters, self).__init__(*args, **kwargs)

    locals().update(filtered_features)

    created_at = filters.DateTimeFilter(method='created_after', label='Created after')
    property_rooms = filters.MultipleChoiceFilter(method='property_rooms_filter',
                                                  choices=[(x, str(x)) if x != 4 else (x, '+' + str(x)) for x in
                                                           range(1, 5)],
                                                  label='Rooms filter')

    property_bathrooms = filters.MultipleChoiceFilter(method='property_bathrooms_filter',
                                                      choices=[(x, str(x)) if x != 3 else (x, '+' + str(x)) for x in
                                                               range(1, 4)],
                                                      label='Bathrooms filter')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(method='price_max_filter', label=_('Price max filter'))
    price_per_sqm_min = filters.NumberFilter(field_name='price_per_sqm', lookup_expr='gte')
    price_per_sqm_max = filters.NumberFilter(field_name='price_per_sqm', lookup_expr='lte')
    price_minimum_min = filters.NumberFilter(field_name='price_minimum', lookup_expr='gte')
    price_minimum_max = filters.NumberFilter(field_name='price_per_sqm', lookup_expr='lte')
    property_type = filters.ChoiceFilter(method='property_type_filter', choices=Property.Type.choices,
                                          label=_('Property type'))
    complex = filters.NumberFilter(method='complex_filter', label='Complex Filter')

    region = filters.NumberFilter(method='property_region_filter', label='Region Filter')
    city = filters.NumberFilter(method='property_city_filter')
    zone = filters.MultipleChoiceFilter(method='property_zone_filter',
                                        choices=list(Zone.objects.values_list('id', 'id')))
    promoted = filters.BooleanFilter(method='property_promoted_filter')
    property_surface_util_min = filters.NumberFilter(method='property_surface_util_min_filter')
    property_surface_util_max = filters.NumberFilter(method='property_surface_util_max_filter')
    property_surface_total_min = filters.NumberFilter(method='property_surface_total_min_filter')
    property_surface_total_max = filters.NumberFilter(method='property_surface_total_max_filter')
    built = filters.ChoiceFilter(method='property_built_filter', choices=settings.BUILT_PERIOD.choices,
                                 label='Built')
    property_comfort = filters.ChoiceFilter(method='property_comfort_filter',
                                            choices=BaseConstructionAttributes.Comfort.choices)
    property_interior_state = filters.ChoiceFilter(method='property_interior_state_filter',
                                                   choices=settings.INTERIOR_STATE.choices)
    property_partitioning = filters.ChoiceFilter(method='property_partitioning_filter',
                                                 choices=BaseConstructionAttributes.Partitioning.choices)
    property_orientation = filters.ChoiceFilter(method='property_orientation_filter',
                                                choices=BaseConstructionAttributes.Orientation.choices)
    property_energy_class = filters.ChoiceFilter(method='property_energy_class_filter',
                                                 choices=BaseConstructionAttributes.EnergyEfficiency.choices,
                                                 label=_('Energy class'))
    property_construction_material = filters.ChoiceFilter(method='property_construction_material_filter',
                                                          choices=settings.CONSTRUCTION_MATERIALS.choices)
    subtype = filters.CharFilter(method='subtype_filter', label=_('Subtype'))

    rental_fund = filters.ChoiceFilter(method='property_apartment_rental_fund_filter',
                                                 choices=ApartmentAttributes.Rental_fund.choices,
                                                 label=_('Rental Fund'))
    apartment_state = filters.ChoiceFilter(method='property_apartment_state_filter',
                                                 choices=ApartmentAttributes.Apartment_state.choices,
                                                 label=_('Apartment State'))
    apartment_construction_material = filters.ChoiceFilter(method='property_apartment_construction_material_filter',
                                                 choices=ApartmentAttributes.Apartment_construction_material.choices,
                                                 label=_('Apartment construction material'))
    apartment_building_plan = filters.ChoiceFilter(method='property_apartment_building_plan_filter',
                                                 choices=ApartmentAttributes.Building_plan.choices,
                                                 label=_('Apartment building plan'))
    house_state = filters.ChoiceFilter(method='property_house_state_filter',
                                                 choices=HouseAttributes.House_state.choices,
                                                 label=_('House state'))
    house_construction_material = filters.ChoiceFilter(method='property_house_construction_material_filter',
                                                 choices=HouseAttributes.House_construction_material.choices,
                                                 label=_('House construction material'))
    commercial_state = filters.ChoiceFilter(method='property_commercial_state_filter',
                                                 choices=CommercialAttributes.Commercial_state.choices,
                                                 label=_('Commercial state'))


    

    class Meta:
        model = Offer
        fields = ['id', 'user', 'type', 'price', 'exclusive', 'special_offer', 'price_per_sqm', 'office']

    def price_max_filter(self, queryset, name, value):
        if value == 500_000:
            return queryset

        return queryset.filter(price__lte=value)

    def created_after(self, queryset, name, value):
        return queryset.filter(created_at__gte=value)

    def property_rooms_filter(self, queryset, name, value):
        qs = None
        for v in value:
            filter = get_property_attributes_filter_queryset('rooms_number', v, is_api_offer_filter=True)
            if not int(v) <= 3:
                filter = get_property_attributes_filter_queryset('rooms_number__gte', 4, is_api_offer_filter=True)

            if not qs:
                qs = Q(filter)
            else:
                qs |= Q(filter)

        return queryset.filter(qs)

    def property_bathrooms_filter(self, queryset, name, value):
        qs = None
        for v in value:
            filter = get_property_attributes_filter_queryset('bathrooms_number', v, is_api_offer_filter=True)
            if not int(v) <= 2:
                filter = get_property_attributes_filter_queryset('bathrooms_number__gte', 3, is_api_offer_filter=True)

            if not qs:
                qs = Q(filter)
            else:
                qs |= Q(filter)

        return queryset.filter(qs)

    def property_type_filter(self, queryset, name, value):
        return queryset.filter(property__type=value)

    def property_region_filter(self, queryset, name, value):
        return queryset.filter(property__region=value)

    def property_city_filter(self, queryset, name, value):
        return queryset.filter(property__city=value)

    def property_zone_filter(self, queryset, name, value):

        qs = None
        for v in value:
            if not qs:
                qs = Q(property__zone=v)
            else:
                qs |= Q(property__zone=v)

        return queryset.filter(qs)

    def property_promoted_filter(self, queryset, name, value):
        return queryset.filter(promoted=value)

    def property_surface_util_min_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('surface_util__gte', value, is_api_offer_filter=True))

    def property_surface_util_max_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('surface_util__lte', value, is_api_offer_filter=True))

    def property_surface_total_min_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('surface_total__gte', value, is_api_offer_filter=True))

    def property_surface_total_max_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('surface_total__lte', value, is_api_offer_filter=True))

    def property_built_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('built', value, is_api_offer_filter=True))

    def property_comfort_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('comfort', value, is_api_offer_filter=True))

    def property_interior_state_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('interior_state', value, is_api_offer_filter=True))

    def property_energy_class_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('energy_class', value, is_api_offer_filter=True))

    def property_construction_material_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('construction_material', value, is_api_offer_filter=True))

    def property_partitioning_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('partitioning', value, is_api_offer_filter=True))

    def property_orientation_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('orientation', value, is_api_offer_filter=True))

    def subtype_filter(self, queryset, name, value):
        return queryset.filter(get_property_attributes_filter_queryset('subtype', value, is_api_offer_filter=True))

    def complex_filter(self, queryset, name, value):
        return queryset.filter(property__complex=value)

    def property_apartment_rental_fund_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('rental_fund', value, is_api_offer_filter=True))

    def property_apartment_state_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('apartment_state', value, is_api_offer_filter=True))
            
    def property_apartment_construction_material_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('apartment_construction_material', value, is_api_offer_filter=True))

    def property_apartment_building_plan_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('building_plan', value, is_api_offer_filter=True))
    
    def property_house_state_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('house_state', value, is_api_offer_filter=True))
    
    def property_house_construction_material_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('house_construction_material', value, is_api_offer_filter=True))
        
    def property_commercial_state_filter(self, queryset, name, value):
        return queryset.filter(
            get_property_attributes_filter_queryset('commercial_state', value, is_api_offer_filter=True))

class StandardPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class OffersListAPIView(BaseListAPIView):
    serializer_class = OfferListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OffersAPIFilters
    pagination_class = StandardPagination

    def get_queryset(self):
        weeks_2_ago = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp() - 3600 * 24 * 14)
        offers_qs = Offer.objects.filter(
            ((Q(status=settings.STATUS.ACTIVE) | Q(status=settings.STATUS.RESERVED)) &
            (Q(promote_site=True) & Q(property__deleted=False)))
             | (Q(status=settings.STATUS.TRANSACTED) & Q(closing_date__gte=weeks_2_ago) & Q(promote_site=True))
        ).order_by(
            '-created_at')

        if self.request.GET.get('sort_by') == 'created_at':
            return offers_qs.order_by('-created_at')

        if self.request.GET.get('sort_by') == 'price_asc':
            return offers_qs.order_by('price')

        if self.request.GET.get('sort_by') == 'price_des':
            return offers_qs.order_by('-price')

        else:
            return offers_qs


class OffersDetailsAPIView(BaseRetrieveAPIView):
    serializer_class = OfferDetailsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OffersAPIFilters

    def get_queryset(self):
        weeks_2_ago = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp() - 3600 * 24 * 14)
        offers_qs = Offer.objects.filter(
            ((Q(status=settings.STATUS.ACTIVE) | Q(status=settings.STATUS.RESERVED)) &
             (Q(promote_site=True) & Q(property__deleted=False)))
            | (Q(status=settings.STATUS.TRANSACTED) & Q(closing_date__gte=weeks_2_ago))
        ).order_by(
            '-created_at')

        return offers_qs


class ExclusiveOffersListAPIView(OffersListAPIView):
    pagination_class = StandardPagination

    def get_queryset(self):
        return super().get_queryset().filter(exclusive=True)


class HomepageOffersListAPIView(OffersListAPIView):
    pagination_class = StandardPagination

    def get_queryset(self):
        return super().get_queryset().filter(homepage=True)


class SpecialOffersListAPIView(OffersListAPIView):
    pagination_class = StandardPagination

    def get_queryset(self):
        return super().get_queryset().filter(special_offer=True)


class RecommendedOffersListAPIView(OffersListAPIView):
    pagination_class = StandardPagination

    def get_queryset(self):
        return super().get_queryset().filter(is_recommended=True)


class TransectedOffersListAPIView(OffersListAPIView):
    pagination_class = StandardPagination

    def get_queryset(self):
        return super().get_queryset().filter(status=settings.STATUS.TRANSACTED).order_by('closing_date')


class ReservedOffersListAPIView(OffersListAPIView):
    pagination_class = StandardPagination

    def get_queryset(self):
        return super().get_queryset().filter(status=settings.STATUS.RESERVED)
