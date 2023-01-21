from crm.api import BaseListAPIView
from properties.models import Feature
from properties.serializers import FeatureSerializer


class FeaturesListAPIView(BaseListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
