from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from offers.models import Offer
from offices.models import Office
from offices.serializers import OfficeSerializer
from properties.models import Property
from properties.serializers import PropertyListSerializer, PropertyDetailsSerializer
from users.models import User
from users.serializers import UserSerializer


class OfferListSerializer(serializers.ModelSerializer):
    property = GenericRelatedField({
        Property: PropertyListSerializer()
    })

    class Meta:
        model = Offer

        fields = ['id', 'status', 'type', 'property', 'price', 'price_old', 'price_hot', 'price_per_sqm', 'exclusive', 'special_offer', 'is_recommended',
                  'homepage', 'created_at', 'display_title', 'closing_date', 'is_closed', 'office', 'casahub', 'makler']


class OfferDetailsSerializer(serializers.ModelSerializer):
    property = GenericRelatedField({
        Property: PropertyDetailsSerializer()
    })

    user = GenericRelatedField({
        User: UserSerializer()
    })

    office = GenericRelatedField({
        Office: OfficeSerializer()
    })

    class Meta:
        model = Offer

        fields = ['id', 'user', 'office', 'status', 'type', 'property', 'price', 'price_old',
                  'price_per_sqm', 'price_hot', 'exclusive', 'special_offer', 'is_recommended', 'homepage',
                  'created_at', 'view_count', 'display_title', 'casahub', 'makler']
