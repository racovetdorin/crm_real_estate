from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from offices.models import Office
from offers.models import Offer
from properties.models import Property
from offices.serializers import OfficeSerializer
from users.models import User, UserImage


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    
    thumbnail = UserImageSerializer(many=False)
    
    office = GenericRelatedField({
        Office: OfficeSerializer()
    })
    
    active_properties = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'active_properties', 'office', 'thumbnail', 'role', 'display_title', 'certificates']

    def get_active_properties(self, obj):
        try:
            return Offer.objects.filter(user=obj, status="active").count()
        except:
            return 0
        
        
