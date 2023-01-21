from crm.utils import set_request, set_office
from django.contrib.auth import logout
from django.conf import settings


class RequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        set_request(request)

        if request.user and not request.user.is_anonymous and request.user.office:
            set_office(request.user.office)

        if request.user and not request.user.is_anonymous and not request.user.is_manager:
            ip = self._get_client_ip(request)

            if settings.ALLOWED_IP != '*' and ip != settings.ALLOWED_IP:
                print(f"blocked ip: {ip}")
                logout(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]

        return request.META.get('REMOTE_ADDR')

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)

        return response

class ForceLangMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META['HTTP_ACCEPT_LANGUAGE'] = "md"
        response = self.get_response(request)
        return response