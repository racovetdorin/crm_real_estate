import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect

from activities.forms import ActivityForm
from activities.models import Activity
from audit.models import AuditLog
from clients.forms import ClientForm
from clients.models import Client
from demands.filters import DemandFilter
from demands.forms import DemandForm, DemandUpdateForm
from demands.models import Demand
from properties.models import Feature, FeatureGroup
from properties.utils import get_properties_queryset, \
    get_activities_context_dict, sort_values, get_activities_ids
from locations.models import Region


class DemandCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Demand
    form_class = DemandForm
    success_message = _('Demand added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DemandForm(initial={'region':Region.objects.get(name='mun. Chișinău'),
                                   'user':self.request.user})
        context['client_form'] = ClientForm
        context['form'] = form
        return context

    def form_valid(self, form):
        demand = form.save(commit=False)
        demand.user = self.request.user
        demand.office = self.request.user.office
        demand.save()
        demand.create_audit(action_type=AuditLog.Type.CREATED)

        return super().form_valid(form)


class DemandUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = Demand
    form_class = DemandUpdateForm
    success_message = _('Demand Updated')

    def post(self, request, *args, **kwargs):
        self.original_user = self.get_object().user

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        
        if form.data.get('is_closed'):
            demand = form.save(commit=False)
            demand.closing_date = datetime.datetime.now()
            if not self.request.user.can_change_agent():
                self.object.user = self.original_user
                self.demand = self.original_user

            if not demand.user:
                self.object.user = self.original_user
                demand.user = self.original_user
            demand.save()
            return redirect('/transacted-demands')

        demand = form.save(commit=False)

        if not self.request.user.can_change_agent():
            self.object.user = self.original_user
            self.demand = self.original_user

        if not demand.user:
            self.object.user = self.original_user
            demand.user = self.original_user

        demand.create_audit(action_type=AuditLog.Type.UPDATED)
        demand.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        demand = self.object
        properties_queryset = get_properties_queryset(demand)

        page = self.request.GET.get('page', 1)

        paginator = Paginator(properties_queryset, settings.DEFAULT_PAGINATION)
        try:
            properties = paginator.page(page)
        except PageNotAnInteger:
            properties = paginator.page(1)
        except EmptyPage:
            properties = paginator.page(paginator.num_pages)

        qs = Activity.objects.filter(demand__id=demand.id, is_archived=False, user=self.request.user).order_by(
            '-created_at')

        activities_context_dict = get_activities_context_dict(qs)
        activities_ids = get_activities_ids(qs)

        filtered_client = None

        if self.request.GET.get('client'):
            filtered_client = Client.objects.filter(id=int(self.request.GET.get('client'))).first()

        context = super().get_context_data(**kwargs)
        context.update({
            'selected_client': demand.client,
            'activity_form': ActivityForm,
            'properties': properties,
            'activities_context_dict': activities_context_dict,
            'storage_url': settings.CDN_MEDIA_URL,
            'client_form': ClientForm,
            'features': Feature.objects.filter(group__property_type__icontains=demand.property_type),
            'feature_groups': FeatureGroup.objects.filter(property_type__icontains=demand.property_type),
            'activity_fk_object_name': self.get_object()._meta.object_name,
            'activity_fk_object_id': self.get_object().id,
            'activities_ids': activities_ids,
            'today': datetime.datetime.now(),
            'filtered_client': filtered_client

        })
        return context

    def get_success_url(self):
        return reverse(settings.DEMANDS_UPDATE_ROUTE, args=[self.object.id])


class DemandSoftDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Demand
    success_message = _('Demand Deleted!')

    def delete(self, request, *args, **kwargs):
        demand = self.get_object()
        demand.deleted = True
        demand.deleted_at = timezone.now()
        demand.create_audit(action_type=AuditLog.Type.DELETED)
        demand.save()

        return HttpResponseRedirect(reverse(settings.DEMANDS_LIST_ROUTE))


class AllDemandListView(LoginRequiredMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION
    model = Demand

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            return Demand.objects.filter(is_closed=False).order_by(sort_by)

        return Demand.objects.filter(is_closed=False).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        filter_form = DemandFilter(self.request.GET, queryset=self.get_queryset())
        features = Feature.objects.filter(is_filtered=True)
        total_demands = filter_form.qs.count()

        context = super().get_context_data(object_list=filter_form.qs, **kwargs)
        context.update({
            'filter': filter_form,
            'sort_values': sort_values,
            'features': features,
            'total_demands': total_demands
        })

        return context


class MyDemandsListView(AllDemandListView):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, is_closed=False)


class OfficeDemandsListView(AllDemandListView):
    def get_queryset(self):
        return super().get_queryset().filter(office=self.request.user.office, is_closed=False)


class TransactedDemandsListView(LoginRequiredMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION
    model = Demand
    transacted_statuses = settings.TRANSACTED_STATUSES

    status_choices = settings.TRANSACTED_STATUSES_CHOICES

    def get_queryset(self):
        return Demand.objects.filter(user=self.request.user, status__in=self.transacted_statuses, is_closed=True).order_by(
            '-closing_date')

    def get_context_data(self, **kwargs):
        filter_form = DemandFilter(self.request.GET, queryset=self.get_queryset())
        context = super().get_context_data(object_list=filter_form.qs, **kwargs)
        context['filter'] = filter_form
        context['status_choices'] = self.status_choices

        return context


class AllTransactedDemandsListView(TransactedDemandsListView):
    def get_queryset(self):
        return Demand.objects.filter(status__in=self.transacted_statuses, is_closed=True).order_by('-closing_date')


def get_demands_by_query(request):
    search_string = request.GET.get('query')
    demands = []

    if search_string:
        demands = Demand.objects.filter(Q(id=int(search_string)) | Q())
    response = {
        'items': [{'id': demand.id,
                   'text': f'{_("Demand")}: {demand.id}'} for demand in demands]}

    return JsonResponse(response)
