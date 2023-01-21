from crm.api import BaseListAPIView
from offices.models import Office
from offices.serializers import OfficeSerializer


class OfficesListAPIView(BaseListAPIView):
    queryset = Office.objects.filter(is_active=True, show_on_site=True).order_by('order')
    serializer_class = OfficeSerializer
