from rest_framework import serializers
from properties.models import ApartmentAttributes, HouseAttributes, CommercialAttributes, StudioAttributes, \
    LandAttributes, HotelAttributes, CabinAttributes, GarageAttributes, BasementParkingAttributes, StorageRoomAttributes, ComplexAttributes

land_fields = ['title', 'description', 'description_sentimental', 'surface_util', 'surface_built', 'front_line',
               'surface_total', 'surface_field']

fields = land_fields + ['partitioning', 'rooms_number', 'comfort', 'floors', 'kitchens_number', 'balconies_number',
                        'orientation',
                        'energy_class', 'top_floor', 'ground_floor', 'mansard', 'new_building', 'in_development',
                        'key_holding', 'internet_connection', 'garage', 'construction_year', 'bathrooms_number',
                        'surface_field', 'surface_garden', 'subtype', 'units_of_measure']


class ApartmentDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAttributes
        fields = fields + ['rental_fund', 'building_plan', 'apartment_state']


class HouseDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseAttributes
        fields = fields + ['house_state']


class LandDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandAttributes
        fields = land_fields + ['units_of_measure']


class StudioDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioAttributes
        fields = fields


class CommercialDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialAttributes
        fields = fields + ['window_shop', 'commercial_state']


class HotelDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAttributes
        fields = fields


class CabinDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinAttributes
        fields = fields


class ComplexDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexAttributes
        fields = fields
        
class GarageDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarageAttributes
        fields = fields


class BasementParkingDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasementParkingAttributes
        fields = fields


class StorageRoomDetailsAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageRoomAttributes
        fields = fields
