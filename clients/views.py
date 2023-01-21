from functools import reduce
from django.db.models import Value as V
from operator import or_

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from activities.forms import ActivityForm
from activities.models import Activity
from audit.models import AuditLog
from clients.filters import ClientFilter
from clients.forms import ClientForm, ClientUpdateForm
from clients.models import Client
from properties.utils import get_activities_context_dict, sort_values, get_activities_ids
from users.models import User
from django.contrib import messages
from offices.models import Office

MAX_NUMBER_OF_RESULTS = 50


class ClientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_message = 'Client Created!'


    def form_valid(self, form):
        
        for client in Client.objects.filter(office=self.request.user.office):
            if form.cleaned_data.get('phone_1') == client.phone_1 and form.cleaned_data.get('prefix_1') == client.prefix_1 or \
                    form.cleaned_data.get('phone_1') == client.phone_1 and form.cleaned_data.get('prefix_1') != client.prefix_1:
                form.add_error(None, _(f'This client already exists, and has been added by {client.user}.'))
                return render(self.request, self.template_name, {'form': form, 'for_creation':True})

        client = form.save(commit=False)
        client.user = self.request.user
        client.office = self.request.user.office

        try:
            client.save()
        except IntegrityError:
            form.add_error(None, _("Client has already been added."))
            return render(self.request, self.template_name, {'form': form, 'for_creation':True})
        messages.success(self.request, self.success_message)
        return render(self.request, self.template_name, {'form':ClientForm(), 'for_creation':True})


    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'for_creation':True})


    def get(self, request, *args, **kwargs):
        form = ClientForm()
        return render(request, self.template_name, {'form':form, 'for_creation':True})


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ClientUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, PassRequestToFormViewMixin, UpdateView):
    def test_func(self):
        return not self.request.user.is_anonymous and self.request.user.can_edit_client(self.get_object())

    model = Client
    form_class = ClientUpdateForm
    success_message = 'Client updated!'


    def get_context_data(self, **kwargs):
        client = self.get_object()
        context = super().get_context_data(**kwargs)
        qs = Activity.objects.filter(client__id=client.id, is_archived=False, user=self.request.user).order_by(
            '-created_at')
        activities_context_dict = get_activities_context_dict(qs)
        activities_ids = get_activities_ids(qs)
        context['activities_context_dict'] = activities_context_dict,
        context['activity_form'] = ActivityForm
        context['activity_fk_object_name'] = client._meta.object_name
        context['activity_fk_object_id'] = client.id
        context['activities_ids'] = activities_ids
        context['current_agent'] = User.objects.get(id=client.user.id)
        context['for_creation'] = False
        return context


    def form_valid(self, form):
        client = self.get_object()
        context = self.get_context_data()

        new_data = context['form']
        
        if self.request.method == 'POST':
            form = ClientUpdateForm(self.request.POST, request=self.request)
        else:
            form = ClientUpdateForm(request=self.request)
        
        # for client in Client.objects.filter(office=self.request.user.office):
        #     if new_data.data.get('phone_1') == client.phone_1 and new_data.data.get('prefix_1') == client.prefix_1 or \
        #             new_data.data.get('phone_1') == client.phone_1 and new_data.data.get('prefix_1') != client.prefix_1:
        #         form.add_error(None, _(f'This client already exists, and has been added by {client.user}.'))
        #         return render(self.request, self.template_name, {'form': form, 'for_creation':False})
        
        client_to_update = Client.objects.get(id=client.id)
        activities_for_client = Activity.objects.filter(client=client_to_update)
        if new_data['agents'].data != '':
            try:
                client_to_update.user = User.objects.get(id=new_data['agents'].data)
                client_to_update.office = client_to_update.user.office
            except User.DoesNotExist:
                pass
        client_to_update.first_name = new_data['first_name'].data
        client_to_update.last_name = new_data['last_name'].data
        client_to_update.email = new_data['email'].data
        client_to_update.phone_1 = new_data['phone_1'].data
        client_to_update.phone_2 = new_data['phone_2'].data
        client_to_update.phone_3 = new_data['phone_3'].data
        client_to_update.prefix_1 = new_data['prefix_1'].data
        client_to_update.prefix_2 = new_data['prefix_2'].data
        client_to_update.prefix_3 = new_data['prefix_3'].data
        client_to_update.company = new_data['company'].data
        client_to_update.is_agency = new_data['is_agency'].data
        client_to_update.is_private = new_data['is_private'].data
        client_to_update.address = new_data['address'].data
        client_to_update.is_owner = new_data['is_owner'].data
        client_to_update.is_buyer = new_data['is_buyer'].data
        client_to_update.save()

        for activity in activities_for_client:
            if client_to_update.phone_1:
                activity.phone = client_to_update.phone_1
            elif client_to_update.phone_2:
                activity.phone = client_to_update.phone_2
            elif client_to_update.phone_3:
                activity.phone = client_to_update.phone_3
            else:
                activity.phone = ''
            activity.save()

        try:
            current_agent = User.objects.get(id=new_data['agents'].data) if new_data['agents'].data != '' else User.objects.get(id=client.user.id)
        except User.DoesNotExist:
            current_agent = ''
        qs = Activity.objects.filter(client__id=client.id, is_archived=False, user=self.request.user).order_by(
            '-created_at')
        activities_context_dict = get_activities_context_dict(qs)
        activities_ids = get_activities_ids(qs)
        context.update({
            'activities_context_dict':activities_context_dict,
            'activity_form':ActivityForm,
            'activity_fk_object_name': client._meta.object_name,
            'activity_fk_object_id': client.id,
            'activities_ids': activities_ids,
            'current_agent': current_agent,
            'for_creation':False
        })

        messages.success(self.request, self.success_message)
        return render(self.request, self.template_name,context)


    def form_invalid(self, form):
        context = self.get_context_data()
        client = self.get_object()

        qs = Activity.objects.filter(client__id=client.id, is_archived=False, user=self.request.user).order_by(
            '-created_at')
        activities_context_dict = get_activities_context_dict(qs)
        activities_ids = get_activities_ids(qs)
        context.update({
            'activities_context_dict': activities_context_dict,
            'activity_form': ActivityForm,
            'activity_fk_object_name': client._meta.object_name,
            'activity_fk_object_id': client.id,
            'activities_ids': activities_ids,
            'current_agent': User.objects.get(id=client.user.id),
            'for_creation':False
        })
        return render(self.request, self.template_name, context)




class ClientSoftDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    def test_func(self):
        return not self.request.user.is_anonymous and self.request.user.can_delete_client(self.get_object())

    model = Client
    success_message = 'Client Deleted!'

    def delete(self, request, *args, **kwargs):
        client = self.get_object()
        client.deleted = True
        client.deleted_at = timezone.now()
        client.create_audit(action_type=AuditLog.Type.DELETED)
        client.save()

        return redirect(settings.CLIENTS_LIST_ROUTE)


class AllClientsListView(LoginRequiredMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION
    model = Client

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            return Client.objects.all().order_by(sort_by)

        return Client.objects.all()

    def get_context_data(self, **kwargs):
        filter_form = ClientFilter(self.request.user, self.request.GET, queryset=self.get_queryset())
        context = super().get_context_data(object_list=filter_form.qs, **kwargs)
        context.update({
            'filter': filter_form,
            'sort_values': sort_values
        })
        return context


class MyClientsListView(AllClientsListView):
    def get_queryset(self):
        return super().get_queryset().filter(Q(user=self.request.user) | Q(is_visible=True))


class OfficeClientsListView(AllClientsListView):
    def get_queryset(self):
        return super().get_queryset().filter(office=self.request.user.office)


@login_required
def get_clients_by_phone(request):
    search_string = request.GET.get('phone')
    if search_string:
        q_object = reduce(or_, (
            Q(first_name__icontains=string) |
            Q(last_name__icontains=string) |
            Q(phone_1__contains=string.lstrip('0')) |
            Q(phone_2__contains=string.lstrip('0')) |
            Q(phone_3__contains=string.lstrip('0'))
            for string in search_string.split()))

        clients = Client.objects.filter(q_object | Q())

    else:
        clients = Client.objects.none()

    if not clients:
        return render(request, 'clients/partials/_empty_dashboard_offers.html')

    context_clients = []
    for client in clients:
        context_clients.append({
            'id': client.id,
            'name': client.get_display_full_name(),
            'phones': client.get_display_phones() if request.user.can_view_client_details(client) else _(
                'Private details for this user'),
            'is_agency': client.is_agency,
            'properties_count': client.properties.count(),
            'demands_count': client.demands.count(),

        })

    return render(request, 'clients/partials/_table_dashboard_offers.html',
                  {'clients': context_clients[:MAX_NUMBER_OF_RESULTS]})


@login_required
def get_clients_by_query(request):
    search_string = request.GET.get('query')
    clients = []
    if search_string:
        if not request.user.is_superuser:
            all_clients = Client.objects.filter(Q(user=request.user) | Q(is_visible=True))
        else:
            all_clients = Client.objects.all()
        annotated_qs = all_clients.annotate(full_name=Concat('first_name', V(' '), 'last_name', V(' ')))
        clients = annotated_qs.filter(full_name__icontains=search_string)

        if not clients:
            q_object = reduce(or_, (
                Q(first_name__icontains=string) |
                Q(last_name__icontains=string) |
                Q(phone_1__icontains=string.lstrip('0')) |
                Q(phone_2__icontains=string.lstrip('0')) |
                Q(phone_3__icontains=string.lstrip('0'))
                for string in search_string.split()))

            if request.user.is_superuser:
                clients = Client.objects.filter(q_object | Q())
            else:
                clients = Client.objects.filter(q_object | Q() , user_id=request.user)

    response = {
        'items': [{'id': client.id,
                   'text': client.get_display_full_name_with_number_email(
                       can_view_details=request.user.can_view_client_details(client))} for client in clients]}

    return JsonResponse(response)
