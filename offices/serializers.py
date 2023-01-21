from rest_framework import serializers
from locations.models import City

from offices.models import Office


class OfficeSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    class Meta:
        model = Office
        fields = ['id', 'name', 'email', 'address', 'show_on_site', 'is_active', 'phone_1', 'order', 'city']
        
    def get_city(self, obj):
        if obj.city_gobal_id:
            return obj.city_gobal_id.name
        else:
            return ''
