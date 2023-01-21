from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from audit.filters import AuditLogFilter
from audit.models import AuditLog


class AuditLogListView(LoginRequiredMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION
    model = AuditLog
    context_object_name = 'logs'

    def get_queryset(self):
        return AuditLog.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        url_routes = (
            ('Property', 'ui:property_update'),
            ('Demand', 'ui:demand_update'),
            ('Client', 'ui:client_update'),
        )

        filter_form = AuditLogFilter(self.request.GET, queryset=self.get_queryset())

        context = super().get_context_data(object_list=filter_form.qs.distinct(), **kwargs)
        context['filter'] = filter_form
        context['url_routes'] = url_routes

        return context

