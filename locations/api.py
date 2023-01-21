from rest_framework.generics import ListAPIView

from crm.api import BaseListAPIView
from locations.models import Region, Zone, City, Street
from locations.serializers import RegionSerializer, CitySerializer, ZoneSerializer, StreetSerializer
from django_filters import rest_framework as filters


class CitiesFilters(filters.FilterSet):
    class Meta:
        model = City
        fields = ['region']


class ZonesFilters(filters.FilterSet):
    class Meta:
        model = Zone
        fields = ['city']


class RegionsListAPIView(BaseListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CitiesListAPIView(BaseListAPIView):
    queryset = City.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CitiesFilters
    serializer_class = CitySerializer


class ZonesListAPIView(BaseListAPIView):
    queryset = Zone.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ZonesFilters
    serializer_class = ZoneSerializer


class StreetsListAPIView(BaseListAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
