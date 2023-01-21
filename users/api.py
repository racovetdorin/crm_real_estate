from crm.api import BaseListAPIView
from users.models import User
from users.serializers import UserSerializer


class UsersListAPIView(BaseListAPIView):
    queryset = User.objects.filter(is_active=True, show_on_site=True)
    serializer_class = UserSerializer
