from rest_framework import serializers
from properties.models import ApartmentAttributes, HouseAttributes, CommercialAttributes, StudioAttributes, \
    LandAttributes, HotelAttributes, GarageAttributes, BasementParkingAttributes, StorageRoomAttributes

fields = ['partitioning', 'surface_util', 'surface_total', 'comfort', 'orientation', 'rooms_number',
          'bathrooms_number', 'interior_state', 'construction_material', 'construction_year', 'energy_class', 'subtype',
          'construction_material', 'units_of_measure']


class ApartmentListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAttributes
        fields = fields + ['rental_fund', 'building_plan', 'apartment_state']


class HouseListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseAttributes
        fields = fields + ['house_state']


class LandListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandAttributes
        fields = ['surface_total', 'surface_util', 'units_of_measure']


class StudioListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioAttributes
        fields = fields


class CommercialListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialAttributes
        fields = fields + ['commercial_state']


class HotelListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAttributes
        fields = fields


class GarageListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarageAttributes
        fields = fields


class BasementParkingListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasementParkingAttributes
        fields = fields


class StorageRoomListAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageRoomAttributes
        fields = fields