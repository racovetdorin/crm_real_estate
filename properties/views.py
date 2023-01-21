import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from activities.filters import ActivityFilter

from activities.forms import ActivityForm
from activities.models import Activity
from audit.models import AuditLog
from clients.forms import ClientForm
from clients.models import Client
from crm.views import ImagesUploadView, DocumentsUploadView
from offers.forms import OfferFormSet
from offers.models import Offer
from locations.models import Region, Street, StreetNumber
from users.models import User

from .filters import PropertyFilter
from .forms import PropertyForm, PropertyUpdateForm
from .models import Property, Feature, FeatureGroup, PropertyImage, PropertyDocument
from .utils import get_attributes_form_for_property_type, get_attributes_form_template_for_property_type, \
    get_demands_queryset, status_check, \
    offer_check, remove_coma, get_activities_context_dict, sort_values, get_coordinates, \
    get_leads_context_dict, get_activities_ids, get_number_of_activites


class PropertyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Property
    form_class = PropertyForm
    success_message = 'Property Created!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_form'] = ClientForm()
        context['form'] = PropertyForm(initial={'region': Region.objects.get(name='mun. Chișinău')})
        return context

    def form_valid(self, form, **kwargs):
        property = form.save(commit=False)
        if self.request.user.role != settings.ROLES.MORTAGE_BROKER:
            property.user = self.request.user
        else:
            ofc_user = User.objects.filter(office__id=self.request.user.office.id, is_active=True).exclude(role=settings.ROLES.MORTAGE_BROKER).exists()
            if ofc_user:
                ofc_user = User.objects.filter(office__id=self.request.user.office.id, is_active=True).exclude(role=settings.ROLES.MORTAGE_BROKER).first()
                property.user = ofc_user
            else:
                property.user = self.request.user

            
        property.office = self.request.user.office

        if not (self.request.POST.get('latitude') and self.request.POST.get('longitude')):
            property.latitude, property.longitude = get_coordinates(property)

        # if self.request.POST.get('street') and self.request.POST.get('city'):
            

        context = super().get_context_data(**kwargs)
        context.update({
            'form': form,
            'client_form': ClientForm
        })

        try:
            property.save()
            property.create_audit(action_type=AuditLog.Type.CREATED)
        except IntegrityError:
            form.add_error(None, _('A property already exists at this address!'))

            return render(self.request, 'properties/add.html', context)

        return super().form_valid(form)


class AgencyPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        if settings.CLIENT == 'ipk':
            return True

        user = self.request.user
        if user.is_superuser:
            return True

        obj = self.get_object()

        if user.office != obj.office:
            return False
        if user.is_manager:
            return True
        if user == obj.user:
            return True


class PropertyUpdateView(LoginRequiredMixin, AgencyPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Property
    form_class = PropertyUpdateForm

    def get_context_data(self, **kwargs):
        property = self.object
        
        demands = get_demands_queryset(property)
        form_activity_error = False
        offers = property.get_last_offers()
        closed_offers = property.offers.filter(is_closed=True)
        if self.request.user.is_superuser or self.request.user.is_manager:
            qs = Activity.objects.filter(property__id=property.id, is_archived=False)
        else:
            qs = Activity.objects.filter(property__id=property.id, is_archived=False, user_id=self.request.user)
        activities_context_dict = get_activities_context_dict(qs)
        leads_context_dict = get_leads_context_dict(qs)
        error = False
        message_error = ''
        if self.request.session.get("form_error") is not None:
            message_error = self.request.session['error_message']
            error = self.request.session['form_error']
            del self.request.session['form_error']
            del self.request.session['error_message']

        activities_ids = get_activities_ids(qs)

        page = self.request.GET.get('page', 1)

        paginator = Paginator(demands, settings.DEFAULT_PAGINATION)
        try:
            demands = paginator.page(page)
        except PageNotAnInteger:
            demands = paginator.page(1)
        except EmptyPage:
            demands = paginator.page(paginator.num_pages)

        context = super().get_context_data(**kwargs)

        status_choices = {}
        offer_creation_status_choices = settings.OFFER_CREATION_STATUS_CHOICES

        for offer in property.offers.values():
            if not self.request.user.is_manager and not offer.get('is_closed'):
                status_choices[str(offer.get('id'))] = settings.STATUS_CONFIG.get(offer.get('status'))
        context.update({
            'images': PropertyImage.objects.filter(property_id=property.id).order_by('position').values(),
            'selected_client': property.client,
            'storage_url': settings.CDN_MEDIA_URL,
            'demands': demands,
            'client_form': ClientForm,
            'feature_groups': FeatureGroup.objects.filter(property_type__contains=property.type),
            'attributes_form': get_attributes_form_for_property_type(property.type)(
                instance=property.attributes_object),
            'attributes_form_template': get_attributes_form_template_for_property_type(property.type),
            'offer_form_set': OfferFormSet(queryset=offers),
            'offers': Offer.objects.filter(property_id=property.id),
            'closed_offers': closed_offers,
            'activities_context_dict': activities_context_dict,
            'leads_context_dict': leads_context_dict,
            'activity_form': ActivityForm,
            'activity_fk_object_name': self.get_object()._meta.object_name,
            'activity_fk_object_id': self.get_object().id,
            'activities_ids': activities_ids,
            'documents': PropertyDocument.objects.filter(property_id=property.id),
            'status_choices': status_choices,
            'offer_creation_status_choices': offer_creation_status_choices,
            'commission_choices': getattr(settings, 'COMMISSION_CHOICES'),
            'google_maps_apikey': settings.GOOGLE_MAPS_API_KEY,
            'activity_form_error': error,
            'activity_form_error_message': message_error,
        })

        return context

    def post(self, request, *args, **kwargs):
        self.original_user = self.get_object().user
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        data = self.request.POST
        if data.get('is_details'):
            property = Property.objects.filter(id=self.object.id).first()
        else:
            property = form.save(commit=False)

        images = []
        deleted_images = []
        all_images = {}
        # print(self.request.POST.get('street'))
        if not self.request.user.can_change_agent():
            self.object.user = self.original_user
            self.property = self.original_user

        if not property.user:
            self.object.user = self.original_user
            property.user = self.original_user

        for key, value in data.items():
            if 'delete-img' in key:
                try:
                    image = PropertyImage.objects.get(id=int(value))
                    image.delete()
                    deleted_images.append(int(value))
                except PropertyImage.DoesNotExist:
                    pass
            elif 'position-img' in key:
                images.append(int(value))
            elif 'hide-img' in key:
                try:
                    image = PropertyImage.objects.get(id=int(value))
                    image.hide_on_site = True
                    image.save()
                except PropertyImage.DoesNotExist:
                    pass


            if 'delete-document' in key:
                try:
                    document = PropertyDocument.objects.get(id=int(value))
                    document.delete()
                except PropertyDocument.DoesNotExist:
                    pass
        
        for deleted_image_id in deleted_images:
            images.remove(deleted_image_id)

        for position, image_id in enumerate(images):
            try:
                image = PropertyImage.objects.get(id=image_id)
                image.position = position
                image.save()
            except PropertyImage.DoesNotExist:
                pass
        

        for image_id in images:
            all_images[f'hide-img-{image_id}'] = 0
        
        for key, value in data.items():
            for k, v in all_images.items():
                if k in key:
                   all_images[k] = 1

        for key, value in all_images.items():
            if value == 0:
                try:
                    key_split = key.split("-")
                    image = PropertyImage.objects.get(id=int(key_split[2]))
                    image.hide_on_site = False
                    image.save()
                except PropertyImage.DoesNotExist:
                    pass

        attributes_form = get_attributes_form_for_property_type(property.type)
        attributes_object = None
        if property.attributes_object:
            attributes_object = property.attributes_object
        attributes_form = attributes_form(self.request.POST, instance=attributes_object)

        demands = get_demands_queryset(property)
        context = self.get_context_data()
        context.update({
            'demands': demands,
            'form': form,
            'property': property,
            'attributes_form': attributes_form,
        })
        
        if attributes_form.is_valid():
            attributes_object = attributes_form.save(commit=False)
            property.create_audit(action_type=AuditLog.Type.ATTRIBUTES_UPDATED, child=attributes_object)
            attributes_object.save()
            property.attributes_object = attributes_object
            property.demands_of_interest.set(self.request.POST.getlist('demands_of_interest'))
            property.create_audit(action_type=AuditLog.Type.UPDATED)
        
        if form.is_valid():
            form_features = self.request.POST.getlist('features')
            
            if form_features:
                property.features.set(int(x) for x in form_features)
            else:
                property.features.set(form_features)

            offers = self.object.get_last_offers()
            offer_form_set = OfferFormSet(remove_coma(self.request.POST), queryset=offers)

            if not offer_form_set.is_valid():
                form.add_error(None, offer_form_set.errors)
                return render(self.request, 'properties/update.html', context)

            offers = offer_form_set.save(commit=False)
            if not offer_check(self.request.POST):
                form.add_error(None, _("There can't be two active offers of the same type!"))
                return render(self.request, 'properties/update.html', context)
            
            for offer in offers:
                
                if isinstance(property, Property) and property.documents.count() == 0 and offer.status in ['active']: 
                    offer.status = settings.STATUS.INCOMPLETE
                    form.add_error(None, _('At least one document is required!'))
                
                if not offer.price and offer.status not in ['incomplete'] and not offer.property:
                    form.add_error(None, _('if you want to add offer you need price'))
                    
                if not offer.price and offer.property:
                    form.add_error(None, _('You cannot leave an already created offer without a price!'))
                    continue
                elif not offer.price:
                    continue
                
                property_offers_ids = [id_dict['id'] for id_dict in property.get_last_offers().values('id')]
                
                if offer.status not in ['active', 'transacted','transacted_by_others', 'transacted_by_us', 'reserved', 'withdrawn']:
                    form.add_error(None, _('Offer status must be "active"'))
                    offer.mls_999 = False
                
                if offer and offer.mls_999:
                    
                    if not attributes_form.is_valid():
                        form.add_error(None, _(f"Completati campurile obligatorii din 'Detalii proprietate' "))
                        offer.mls_999 = False
                        
                    if offer.property.type == 'apartment':
                        if offer.property.floor is None:
                            form.add_error(None, _('Fill in the field "Floor!"'))
                            offer.mls_999 = False
                        if offer.price is None:
                            form.add_error(None, _('Fill in the field "Offer price!"'))
                            offer.mls_999 = False
                        if offer.property.region is None:
                            form.add_error(None, _('Fill in the field "Region!"'))
                            offer.mls_999 = False
                        if offer.property.city is None:
                            form.add_error(None, _('Fill in the field "City!"'))
                            offer.mls_999 = False
                        if offer.property.zone is None:
                            form.add_error(None, _('Fill in the field "Zone!"'))
                            offer.mls_999 = False
                        if offer.property.street is None:
                            form.add_error(None, _('Fill in the field "Street!"'))
                            offer.mls_999 = False
                        if offer.property.street_number is None:
                            form.add_error(None, _('Fill in the field "Street number!"'))
                            offer.mls_999 = False
                            
                        images = PropertyImage.objects.filter(property=offer.property, hide_on_site=False)
                        
                        if len(images) == 0:
                            form.add_error(None, _('You cannot promote a property without images!'))
                            offer.mls_999 = False
                        if offer.type == 'rent' and offer.property.attributes_object.allow_childrens is None:
                            form.add_error(None, _('Fill in the field "Allow Childrens!"'))
                            offer.mls_999 = False
                        if offer.type == 'rent' and offer.property.attributes_object.allow_animals is None:
                            form.add_error(None, _('Fill in the field "Allow Animals!"'))
                            offer.mls_999 = False
                    
                    if offer.property.type == 'house':
                        if offer.property.region is None:
                            form.add_error(None, _('Fill in the field "Region!"'))
                            offer.mls_999 = False
                        if offer.property.city is None:
                            form.add_error(None, _('Fill in the field "City!"'))
                            offer.mls_999 = False
                        if offer.property.zone is None:
                            form.add_error(None, _('Fill in the field "Zone!"'))
                            offer.mls_999 = False
                        if offer.property.street is None:
                            form.add_error(None, _('Fill in the field "Street!"'))
                            offer.mls_999 = False
                        if offer.property.street_number is None:
                            form.add_error(None, _('Fill in the field "Street number!"'))
                            offer.mls_999 = False
                            
                        images = PropertyImage.objects.filter(property=offer.property, hide_on_site=False)
                        
                        if len(images) == 0:
                            form.add_error(None, _('You cannot promote a property without images!'))
                            offer.mls_999 = False
                        if offer.type == 'rent' and offer.property.attributes_object.allow_childrens is None:
                            form.add_error(None, _('Fill in the field "Allow Childrens!"'))
                            offer.mls_999 = False
                        if offer.type == 'rent' and offer.property.attributes_object.allow_animals is None:
                            form.add_error(None, _('Fill in the field "Allow Animals!"'))
                            offer.mls_999 = False

                    if offer.property.type == 'land':
                        images = PropertyImage.objects.filter(property=offer.property, hide_on_site=False)
                        if len(images) == 0:
                            form.add_error(None, _('You cannot promote a property without images!'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.subtype is None:
                            form.add_error(None, _('Fill in the field "Land subtype!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.surface_total is None:
                            form.add_error(None, _('Fill in the field "Total Surface!"'))
                            offer.mls_999 = False
                        if offer.property.region is None:
                            form.add_error(None, _('Fill in the field "Region!"'))
                            offer.mls_999 = False
                        if offer.property.city is None:
                            form.add_error(None, _('Fill in the field "City!"'))
                            offer.mls_999 = False
                        if offer.property.zone is None:
                            form.add_error(None, _('Fill in the field "Zone!"'))
                            offer.mls_999 = False
                        if offer.property.street is None:
                            form.add_error(None, _('Fill in the field "Street!"'))
                            offer.mls_999 = False
                        if offer.property.street_number is None:
                            form.add_error(None, _('Fill in the field "Street number!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.description_sentimental is None:
                            form.add_error(None, _('Fill in the field "Description sentimental!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.description is None:
                            form.add_error(None, _('Fill in the field "Description public!"'))
                            offer.mls_999 = False
                
                    if offer.property.type in ['basement_parking', 'garage']:
                        if offer.property.attributes_object.description_sentimental is None:
                            form.add_error(None, _('Fill in the field "Description sentimental!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.description is None:
                            form.add_error(None, _('Fill in the field "Description public!"'))
                            offer.mls_999 = False
                        if offer.property.region is None:
                            form.add_error(None, _('Fill in the field "Region!"'))
                            offer.mls_999 = False
                        if offer.property.city is None:
                            form.add_error(None, _('Fill in the field "City!"'))
                            offer.mls_999 = False
                        if offer.property.zone is None:
                            form.add_error(None, _('Fill in the field "Zone!"'))
                            offer.mls_999 = False
                        if offer.property.street is None:
                            form.add_error(None, _('Fill in the field "Street!"'))
                            offer.mls_999 = False
                        if offer.property.street_number is None:
                            form.add_error(None, _('Fill in the field "Street number!"'))
                            offer.mls_999 = False
                
                    if offer.property.type == 'commercial':
                        if offer.property.attributes_object.subtype is None:
                            form.add_error(None, _('Fill in the field "Commercial subtype!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.surface_total is None:
                            form.add_error(None, _('Fill in the field "Total Surface!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.commercial_state is None:
                            form.add_error(None, _('Fill in the field "Interior state!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.surface_util is None:
                            form.add_error(None, _('Fill in the field "Surface Util!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.description_sentimental is None:
                            form.add_error(None, _('Fill in the field "Description sentimental!"'))
                            offer.mls_999 = False
                        if offer.property.attributes_object.description is None:
                            form.add_error(None, _('Fill in the field "Description public!"'))
                            offer.mls_999 = False
                        if offer.property.region is None:
                            form.add_error(None, _('Fill in the field "Region!"'))
                            offer.mls_999 = False
                        if offer.property.city is None:
                            form.add_error(None, _('Fill in the field "City!"'))
                            offer.mls_999 = False
                        if offer.property.zone is None:
                            form.add_error(None, _('Fill in the field "Zone!"'))
                            offer.mls_999 = False
                        if offer.property.street is None:
                            form.add_error(None, _('Fill in the field "Street!"'))
                            offer.mls_999 = False
                        if offer.property.street_number is None:
                            form.add_error(None, _('Fill in the field "Street number!"'))
                            offer.mls_999 = False

                if offer.is_closed is True and 'is_created' in offer.mls_999_data.keys():
                        offer.mls_999 = False
                        offer.mls_999_data = {}
                        offer.mls_999_data['is_closed'] = True
                        form.add_error(None, _(f"Offer has been closed, please unpromote offer from 999.md"))
                        
                if offer.id not in property_offers_ids and len(property.get_last_offers().values()) >= 2:
                    form.add_error(None, _('Property should not have more than two offers!'))
                    property.save()
                    messages.success(self.request, _('Property updated!'))
                    return render(self.request, 'properties/update.html', context)

                offer.property = property
                offer.user = property.user
                offer.office = property.user.office

                if status_check(offer):
                    if offer.is_closed and offer.status == settings.STATUS.ACTIVE:
                        offer.is_closed = False
                        offer.closed_by = ''
                        form.add_error(None,
                                       _('Cannot close an active offer. Change the status to a transacted or withdrawn.'))
                else:
                    try:
                        offer.status = offer.diff['status'][0]
                    except Exception:
                        pass

                    offer.status = settings.STATUS.INCOMPLETE
                    form.add_error(None, _(
                        f'Offer not ready to be active or transacted! The Property must have a Description and the Offer must have a Price.'))

                if offer.is_closed and not offer.final_price and not offer.commission:
                    offer.is_closed = False
                    form.add_error(None,
                                   _('You cannot close an offer without completing the final price and the commission'))

                if (self.request.POST.get('form-0-is_closed') or self.request.POST.get(
                        'form-1-is_closed')) and not offer.closing_date:
                    offer.closing_date = datetime.datetime.now()

                if offer.promote_site is False:
                    offer.mls_remax_global = False

                if offer.promote_site:
                    images = PropertyImage.objects.filter(property=property)
                    if len(images) == 0:
                        form.add_error(None,
                                       _('You cannot promote on website a property that does not have images uploaded!')
                                       )
                        offer.promote_site = False
                        offer.mls_remax_global = False
                        if offer.id:
                            property.create_audit(action_type=AuditLog.Type.OFFER_UPDATED, child=offer)
                            offer.save()

                        else:
                            offer.save()
                            property.create_audit(action_type=AuditLog.Type.OFFER_CREATED, child=offer)

                        property.save()
                        messages.success(self.request, _('Property updated!'))
                        return render(self.request, 'properties/update.html', context)

                if offer.id:
                    property.create_audit(action_type=AuditLog.Type.OFFER_UPDATED, child=offer)
                    offer.save()

                else:
                    offer.save()
                    property.create_audit(action_type=AuditLog.Type.OFFER_CREATED, child=offer)
                context['status_choices'].update({str(offer.id): settings.STATUS_CONFIG.get(offer.status)})

            property.save()
            messages.success(self.request, _('Property updated!'))

        return render(self.request, 'properties/update.html', context)


class PropertySoftDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Property
    success_message = 'Property deleted!'

    def delete(self, request, *args, **kwargs):
        property = self.get_object()
        property.deleted = True
        property.deleted_at = timezone.now()
        property.create_audit(action_type=AuditLog.Type.DELETED)
        property.save()
        return redirect(settings.PROPERTIES_LIST_ROUTE)


class AllPropertiesListView(LoginRequiredMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION
    model = Property

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            return Property.objects.all().order_by(sort_by)
        return Property.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        filter_form = PropertyFilter(self.request.GET, queryset=self.get_queryset())

        if self.request.user.groups.values_list():
            groups = self.request.user.groups.values_list()
        else:
            groups = []

        features = Feature.objects.filter(is_filtered=True)

        filtered_properties_with_open_offers = filter_form.qs.select_related('offers').filter(offers__is_closed=False)
        total_offers = filtered_properties_with_open_offers.annotate(total=Count('offers')).count()

        filtered_client = None
        user_office = self.request.user.office
        offices_properties = filter_form.qs.filter(office=user_office)

        if self.request.GET.get('client'):
            filtered_client = Client.objects.filter(id=int(self.request.GET.get('client'))).first()

        context = super().get_context_data(object_list=filter_form.qs.distinct(), **kwargs)
        context.update({
            'total_properties': filter_form.qs.count(),
            'filter': filter_form,
            'groups': groups,
            'features': features,
            'storage_url': settings.CDN_MEDIA_URL,
            'sort_values': sort_values,
            'total_offers': total_offers,
            'today': datetime.datetime.now(),
            'filtered_client': filtered_client,
            'offices_properties': offices_properties
        })

        return context


class MyPropertiesListView(AllPropertiesListView):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OfficePropertiesListView(AllPropertiesListView):
    def get_queryset(self):
        return super().get_queryset().filter(office=self.request.user.office)


class PropertyImagesUploadView(ImagesUploadView):
    IMAGE_MODEL = PropertyImage
    OBJECT_MODEL = Property
    STORAGE_LOCATION = settings.STORAGE_LOCATION
    OBJECT_TYPE_STRING = 'property'


class PropertyDocumentsUploadView(DocumentsUploadView):
    DOCUMENT_MODEL = PropertyDocument
    OBJECT_MODEL = Property
    DOCUMENTS_STORAGE_LOCATION = settings.DOCUMENTS_STORAGE_LOCATION
    OBJECT_TYPE_STRING = 'property'


class PropertyGenerateRecordView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Property
    form_class = PropertyUpdateForm

    def get_context_data(self, **kwargs):
        property = self.object
        demands = get_demands_queryset(property)
        offers = property.get_last_offers()
        closed_offers = property.offers.filter(is_closed=True)
        report_start_date = property.report_start_date
        report_end_date = property.report_end_date
        if report_start_date is not None or report_end_date is not None:
            report_start_date_range = datetime.datetime(report_start_date.year,report_start_date.month,
                                                  report_start_date.day,23,59,59)
            report_end_date_range = datetime.datetime(report_end_date.year, report_end_date.month,
                                                  report_end_date.day, 23, 59, 59)
            qs = Activity.objects.filter(property__id=property.id, is_archived=False, created_at__gte=report_start_date_range,
                                         created_at__lte=report_end_date_range).order_by('-created_at')
        else:
            qs = Activity.objects.filter(property__id=property.id, is_archived=False).order_by('-created_at')
        activities_context_dict = get_activities_context_dict(qs)
        # print(list(activities_context_dict['done']['qs']), flush=True)
        activites = get_number_of_activites(list(activities_context_dict['done']['qs']))
        leads_context_dict = get_leads_context_dict(qs)
        leads_processed = get_number_of_activites(list(leads_context_dict['processed']['qs']))
        leads_rent = get_number_of_activites(list(leads_context_dict['rent_offers']['qs']))
        leads_sale = get_number_of_activites(list(leads_context_dict['sale_offers']['qs']))
        leads = {**leads_processed, **leads_rent, **leads_sale}
        number_of_done_activities = len(activities_context_dict['done']['qs'])
        number_of_in_progress_activities = len(activities_context_dict['in_progress']['qs'])
        number_of_to_do_activities = len(activities_context_dict['to_do']['qs'])
        number_of_leads = len(leads_context_dict['sale_offers']['qs']) + len(leads_context_dict['rent_offers']['qs']) + len(leads_context_dict['processed']['qs'])
        total_number_of_activities = number_of_done_activities + number_of_leads
        activities_ids = get_activities_ids(qs)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(demands, settings.DEFAULT_PAGINATION)
        try:
            demands = paginator.page(page)
        except PageNotAnInteger:
            demands = paginator.page(1)
        except EmptyPage:
            demands = paginator.page(paginator.num_pages)

        context = super().get_context_data(**kwargs)

        status_choices = {}
        offer_creation_status_choices = settings.OFFER_CREATION_STATUS_CHOICES

        for offer in property.offers.values():
            if not self.request.user.is_manager and not offer.get('is_closed'):
                status_choices[str(offer.get('id'))] = settings.STATUS_CONFIG.get(offer.get('status'))

        context.update({
            'images': PropertyImage.objects.filter(property_id=property.id).order_by('position').values(),
            'selected_client': property.client,
            'storage_url': settings.CDN_MEDIA_URL,
            'activities_type_list': activites,
            'leads_type_list': leads,
            'demands': demands,
            'client_form': ClientForm,
            'feature_groups': FeatureGroup.objects.all(),
            'attributes_form': get_attributes_form_for_property_type(property.type)(
                instance=property.attributes_object),
            'attributes_form_template': get_attributes_form_template_for_property_type(property.type),
            'offer_form_set': OfferFormSet(queryset=offers),
            'offers': Offer.objects.filter(property_id=property.id),
            'closed_offers': closed_offers,
            'activities_context_dict': activities_context_dict,
            'leads_context_dict': leads_context_dict,
            'activity_form': ActivityForm,
            'activity_fk_object_name': self.get_object()._meta.object_name,
            'activity_fk_object_id': self.get_object().id,
            'activities_ids': activities_ids,
            'documents': PropertyDocument.objects.filter(property_id=property.id),
            'status_choices': status_choices,
            'offer_creation_status_choices': offer_creation_status_choices,
            'commission_choices': getattr(settings, 'COMMISSION_CHOICES'),
            'number_of_done_activities': number_of_done_activities,
            'number_of_in_progress_activities': number_of_in_progress_activities,
            'number_of_to_do_activities': number_of_to_do_activities,
            'total_number_of_activities': total_number_of_activities,

        })

        return context

    def post(self, request, *args, **kwargs):
        self.original_user = self.get_object().user
        return super().post(request, *args, **kwargs)


def get_properties_by_query(request):
    search_string = request.GET.get('query')
    properties = []

    if search_string:
        properties = Property.objects.filter(Q(id=int(search_string)) | Q())
    response = {
        'items': [{'id': property.id,
                   'text': f'{_("Property")}: {property.id}'} for property in properties]}

    return JsonResponse(response)


def get_properties_by_offer_id_query(request):
    search_string = request.GET.get('query')
    properties = []

    if search_string:
        properties = Property.objects.filter(Q(offers_id=int(search_string)) | Q())
    response = {
        'items': [{'id': property.id,
                   'text': f'{_("Property")}: {property.id}, Offer: {search_string}'} for property in properties]}

    return JsonResponse(response)
