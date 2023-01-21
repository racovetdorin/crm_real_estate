from rest_framework import serializers
from crm.filters import get_details_medium_watermarked_thumbnail_url
from generic_relations.relations import GenericRelatedField

from locations.models import Region, City, Zone, Street
from locations.serializers import RegionSerializer, CitySerializer, ZoneSerializer, StreetSerializer
from properties.api_attributes_object.api_details_attributes_object import ApartmentDetailsAttributesSerializer, \
    HouseDetailsAttributesSerializer, StudioDetailsAttributesSerializer, CommercialDetailsAttributesSerializer, \
    LandDetailsAttributesSerializer, HotelDetailsAttributesSerializer, CabinDetailsAttributesSerializer, \
    GarageDetailsAttributesSerializer, BasementParkingDetailsAttributesSerializer, StorageRoomDetailsAttributesSerializer, ComplexDetailsAttributesSerializer
from properties.api_attributes_object.api_list_attributes_object import ApartmentListAttributesSerializer, \
    HouseListAttributesSerializer, StudioListAttributesSerializer, CommercialListAttributesSerializer, \
    LandListAttributesSerializer, HotelListAttributesSerializer, GarageListAttributesSerializer, \
    BasementParkingListAttributesSerializer, StorageRoomListAttributesSerializer
from properties.models import Property, ApartmentAttributes, HouseAttributes, CommercialAttributes, StudioAttributes, \
    LandAttributes, HotelAttributes, PropertyImage, Feature, CabinAttributes, GarageAttributes, BasementParkingAttributes, \
    StorageRoomAttributes, ComplexAttributes


class PropertyImageSerializer(serializers.ModelSerializer):
    
    thumbnail_path = serializers.SerializerMethodField()
    class Meta:
        model = PropertyImage
        fields = '__all__'
        
    def get_thumbnail_path(self, obj):
        return get_details_medium_watermarked_thumbnail_url(obj.image_path, True)
        

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'group', 'is_filtered']


class PropertyListSerializer(serializers.ModelSerializer):
    attributes_object = GenericRelatedField({
        ApartmentAttributes: ApartmentListAttributesSerializer(),
        HouseAttributes: HouseListAttributesSerializer(),
        StudioAttributes: StudioListAttributesSerializer(),
        CommercialAttributes: CommercialListAttributesSerializer(),
        LandAttributes: LandListAttributesSerializer(),
        HotelAttributes: HotelListAttributesSerializer(),
        CabinAttributes: CabinDetailsAttributesSerializer(),
        ComplexAttributes: ComplexDetailsAttributesSerializer(),
        GarageAttributes: GarageListAttributesSerializer(),
        BasementParkingAttributes: BasementParkingListAttributesSerializer(),
        StorageRoomAttributes: StorageRoomListAttributesSerializer()
    })

    city = GenericRelatedField({
        City: CitySerializer()
    })

    zone = GenericRelatedField({
        Zone: ZoneSerializer()
    })
    
    

    public_images = PropertyImageSerializer(many=True)
    thumbnail = PropertyImageSerializer()

    features = FeatureSerializer(many=True)

    class Meta:
        model = Property
        fields = ['attributes_object', 'city', 'zone', 'features', 'public_images', 'thumbnail']


class PropertyDetailsSerializer(serializers.ModelSerializer):
    attributes_object = GenericRelatedField({
        ApartmentAttributes: ApartmentDetailsAttributesSerializer(),
        HouseAttributes: HouseDetailsAttributesSerializer(),
        StudioAttributes: StudioDetailsAttributesSerializer(),
        CommercialAttributes: CommercialDetailsAttributesSerializer(),
        LandAttributes: LandDetailsAttributesSerializer(),
        HotelAttributes: HotelDetailsAttributesSerializer(),
        CabinAttributes: CabinDetailsAttributesSerializer(),
        ComplexAttributes: ComplexDetailsAttributesSerializer(),
        GarageAttributes: GarageDetailsAttributesSerializer(),
        BasementParkingAttributes: BasementParkingDetailsAttributesSerializer(),
        StorageRoomAttributes: StorageRoomDetailsAttributesSerializer()

    })

    region = GenericRelatedField({
        Region: RegionSerializer()
    })

    city = GenericRelatedField({
        City: CitySerializer()
    })

    zone = GenericRelatedField({
        Zone: ZoneSerializer()
    })

    street = GenericRelatedField({
        Street: StreetSerializer()
    })

    public_images = PropertyImageSerializer(many=True)

    features = FeatureSerializer(many=True)

    class Meta:
        model = Property
        fields = ['attributes_object', 'id', 'type', 'virtual_tour', 'video_tour', 'floor', 'created_at', 'region',
                  'city', 'zone', 'street', 'public_images', 'features', 'latitude', 'longitude']
