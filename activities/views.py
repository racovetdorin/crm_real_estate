from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from django.utils.translation import ugettext as _
from django.db import IntegrityError

from activities.filters import ActivityFilter
from activities.forms import ActivityForm
from activities.models import Activity
from audit.models import AuditLog
from clients.models import Client
from crm.utils import get_user
from demands.models import Demand
from properties.models import Property
from properties.utils import get_activities_context_dict, activities_statuses, leads_statuses, get_leads_context_dict, \
    get_activities_ids
from django.shortcuts import render



@login_required
def activity_create(request):
    activity_obj = Activity.objects.filter(id=request.GET.get('activity_id')).first()
    current_path = request.POST.get('current_path')

    if activity_obj:
        form = ActivityForm(data=request.POST, instance=activity_obj)

        if form.is_valid():
            activity = form.save(commit=False)

            if request.POST.get('is_taken'):
                activity.user = get_user()

            activity.create_audit(action_type=AuditLog.Type.UPDATED)

            if activity.client:
                if activity.client.phone_1:
                    activity.phone = activity.client.phone_1
                elif activity.client.phone_2:
                    activity.phone = activity.client.phone_2
                elif activity.client.phone_3:
                    activity.phone = activity.client.phone_3
            if activity.user is None or activity.user == '':
                activity.user = request.user
            activity.save()
        else:
            print(form.errors)
            request.session['error_message'] = list(dict(form.errors.get_json_data(escape_html=False)).values())[0][0]['message']
            request.session['form_error'] = True

    else:
        form = ActivityForm(data=request.POST)
        if form.is_valid():
            activity = form.save(commit=False)

            linked_with = []
            if activity.property:
                linked_with.append('property')
            if activity.client:
                linked_with.append('client')
            if activity.demand:
                linked_with.append('demand')

            activity.linked_with = linked_with

            if request.POST.get('activity_fk_object_model_name'):
                fk_object_types = {
                    'Property': ('property', Property),
                    'Demand': ('demand', Demand),
                    'Client': ('client', Client)
                }
                fk_object_model_name = request.POST.get('activity_fk_object_model_name')
                fk_object_id = request.POST.get('activity_fk_object_id')

                fk_object_type = fk_object_types[fk_object_model_name][0]
                fk_object = fk_object_types[fk_object_model_name][1].objects.filter(id=fk_object_id).first()

                activity.linked_with = [fk_object_type]

                setattr(activity, fk_object_type, fk_object)

            if activity.client:
                if activity.client.phone_1:
                    activity.phone = activity.client.phone_1
                elif activity.client.phone_2:
                    activity.phone = activity.client.phone_2
                elif activity.client.phone_3:
                    activity.phone = activity.client.phone_3
            if activity.user is None or activity.user == '':
                activity.user = request.user
            activity.save()
            activity.create_audit(action_type=AuditLog.Type.CREATED)
        else:
            request.session['error_message'] = list(dict(form.errors.get_json_data(escape_html=False)).values())[0][0]['message']
            request.session['form_error'] = True

    return redirect(current_path)


class BaseActivitiesListView(LoginRequiredMixin, ListView):
    model = Activity

    def get_context_data(self, **kwargs):
        filter_form = ActivityFilter(self.request.GET, queryset=self.get_queryset())
        activities_context_dict = get_activities_context_dict(filter_form.qs)

        activities_ids = get_activities_ids(filter_form.qs)

        filtered_client = None
        filtered_property = None
        error = False
        message_error = ''
        if self.request.session.get("form_error") is not None:
            message_error = self.request.session['error_message']
            error = True
            del self.request.session['form_error']
            del self.request.session['error_message']

        if self.request.GET.get('client'):
            filtered_client = Client.objects.filter(id=int(self.request.GET.get('client'))).first()

        if self.request.GET.get('property'):
            filtered_property = Property.objects.filter(id=int(self.request.GET.get('property'))).first()

        context = super().get_context_data(object_list=filter_form.qs, **kwargs)
        context.update({
            'filter': filter_form,
            'activities_context_dict': activities_context_dict,
            'activities_ids': activities_ids,
            'form': ActivityForm,
            'activities': True,
            'filtered_client': filtered_client,
            'filtered_property': filtered_property,
            'err':error,
            'message_error':message_error
        })

        return context


class MyActivitiesListView(BaseActivitiesListView):
    def get_queryset(self):
        qs = Activity.objects.filter(status__in=activities_statuses, user=self.request.user,
                                     is_archived=False).order_by('-created_at')

        if self.request.user.is_superuser:
            return qs

        return qs if settings.CLIENT == 'rmm' else qs.filter(is_available=True)


class AllActivitiesListView(BaseActivitiesListView):
    def get_queryset(self):
        qs = Activity.objects.filter(status__in=activities_statuses, is_archived=False).order_by('-created_at')

        if self.request.user.is_superuser or self.request.user.is_manager:
            return qs

        return qs.filter(is_available=True)


class ArchivedActivitiesListView(BaseActivitiesListView):
    paginate_by = settings.DEFAULT_PAGINATION

    def get_queryset(self):
        qs = Activity.objects.filter(status__in=activities_statuses, is_archived=True).order_by(
            '-created_at')

        if settings.CLIENT == 'rmm' and not self.request.user.is_manager:
            qs = Activity.objects.filter(status__in=activities_statuses, is_archived=True,
                                         user=self.request.user).order_by(
                '-created_at')

        return qs


class BaseLeadsListView(LoginRequiredMixin, ListView):
    model = Activity
 
    def get_context_data(self, **kwargs):
        error = False
        message_error = ''
        if self.request.session.get("form_error") is not None:
            message_error = self.request.session['error_message']
            error = True
            del self.request.session['form_error']
            del self.request.session['error_message']
        
        filter_form = ActivityFilter(self.request.GET, queryset=self.get_queryset())
        activities_context_dict = get_leads_context_dict(filter_form.qs)

        filtered_client = None
        filtered_property = None

        if self.request.GET.get('client'):
            filtered_client = Client.objects.filter(id=int(self.request.GET.get('client'))).first()

        if self.request.GET.get('property'):
            filtered_property = Property.objects.filter(id=int(self.request.GET.get('property'))).first()

        context = super().get_context_data(object_list=filter_form.qs, **kwargs)
        context.update({
            'filter': filter_form,
            'activities_context_dict': activities_context_dict,
            'form': ActivityForm,
            'leads': True,
            'filtered_client': filtered_client,
            'filtered_property': filtered_property,
            'err':error,
            'message_error':message_error
        })
        return context


class MyLeadsListView(BaseLeadsListView):
    def get_queryset(self):
        qs = Activity.objects.filter(status__in=leads_statuses, user=self.request.user, is_archived=False)
        if self.request.user.is_superuser:
            return qs

        return qs if settings.CLIENT == 'rmm' else qs.filter(is_available=True)


class AllLeadsListView(BaseLeadsListView):
    def get_queryset(self):
        qs = Activity.objects.filter(status__in=leads_statuses, is_archived=False)

        if self.request.user.is_superuser or self.request.user.is_manager:
            return qs

        return qs.filter(is_available=True)


class ArchivedLeadsListView(BaseLeadsListView):
    paginate_by = settings.DEFAULT_PAGINATION

    def get_queryset(self):
        qs = Activity.objects.filter(status__in=leads_statuses, is_archived=True).order_by(
            '-created_at')

        if settings.CLIENT == 'rmm' and not self.request.user.is_manager:
            qs = Activity.objects.filter(status__in=leads_statuses, is_archived=True, user=self.request.user).order_by(
                '-created_at')

        return qs


@login_required
def archive_activities(request):
    if request.POST.get('leads'):
        Activity.objects.filter(status=Activity.Status.PROCESSED, user=request.user).update(is_archived=True)

        return redirect(settings.MY_LEADS_LIST_ROUTE)

    if request.POST.get('activities'):
        Activity.objects.filter(status=Activity.Status.DONE, user=request.user).update(is_archived=True)

        return redirect(settings.MY_ACTIVITIES_LIST_ROUTE)

    return HttpResponse(_("Something went terribly wrong!!!"))
