from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from offers.models import Offer


class BaseListAPIView(ListAPIView):
    permission_classes = [HasAPIKey | IsAuthenticated]


class BaseRetrieveAPIView(RetrieveAPIView):
    permission_classes = [HasAPIKey | IsAuthenticated]
