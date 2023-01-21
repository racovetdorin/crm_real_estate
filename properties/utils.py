import requests
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import ugettext as _

from activities.models import Activity
from clients.forms import ClientForm
from clients.models import Client
from demands.models import Demand
from offers.models import Offer
from properties.forms import ApartmentAttributesForm, HouseAttributesForm, StudioAttributesForm, \
    CommercialAttributesForm, LandAttributesForm, HotelAttributesForm, CabinAttributesForm, StorageRoomAttributesForm, \
    GarageAttributesForm, BasementParkingAttributesForm, ComplexAttributesForm
from properties.models import Property, ApartmentAttributes, HouseAttributes, StudioAttributes, CommercialAttributes, \
    LandAttributes, HotelAttributes, Feature, StorageRoomAttributes, GarageAttributes, BasementParkingAttributes, ComplexAttributes


def get_attributes_form_for_property_type(type):
    switcher = {
        Property.Type.APARTMENT: ApartmentAttributesForm,
        Property.Type.HOUSE: HouseAttributesForm,
        Property.Type.STUDIO: StudioAttributesForm,
        Property.Type.COMMERCIAL: CommercialAttributesForm,
        Property.Type.LAND: LandAttributesForm,
        Property.Type.HOTEL: HotelAttributesForm,
        Property.Type.CABIN: CabinAttributesForm,
        Property.Type.COMPLEX: ComplexAttributesForm,
        Property.Type.BASEMENT_PARKING: BasementParkingAttributesForm,
        Property.Type.GARAGE: GarageAttributesForm,
        Property.Type.STORAGE_ROOM: StorageRoomAttributesForm,

    }

    try:
        if type in switcher.keys():
            return switcher.get(type)
    except KeyError:
        raise KeyError(
            'Wrong key in property type switcher dictionary (properties.utils.get_attributes_form_for_property_type'
        )


def get_attributes_form_template_for_property_type(type):
    switcher = {
        Property.Type.APARTMENT: 'properties/attributes/apartment_form.html',
        Property.Type.HOUSE: 'properties/attributes/house_form.html',
        Property.Type.STUDIO: 'properties/attributes/studio_form.html',
        Property.Type.COMMERCIAL: 'properties/attributes/commercial_form.html',
        Property.Type.LAND: 'properties/attributes/land_form.html',
        Property.Type.HOTEL: 'properties/attributes/hotel_form.html',
        Property.Type.CABIN: 'properties/attributes/cabin_form.html',
        Property.Type.COMPLEX: 'properties/attributes/complex_form.html',
        Property.Type.BASEMENT_PARKING: 'properties/attributes/basement_parking_form.html',
        Property.Type.STORAGE_ROOM: 'properties/attributes/storage_room_form.html',
        Property.Type.GARAGE: 'properties/attributes/garage_form.html',
    }

    try:
        if type in switcher.keys():
            return switcher.get(type)
    except KeyError:
        raise KeyError(
            'Wrong key in property type switcher dictionary (properties.utils.'
            'get_attributes_form_template_for_property_type'
        )


def get_attributes_object(type):
    switcher = {
        Property.Type.APARTMENT: ApartmentAttributes,
        Property.Type.HOUSE: HouseAttributes,
        Property.Type.STUDIO: StudioAttributes,
        Property.Type.COMMERCIAL: CommercialAttributes,
        Property.Type.LAND: LandAttributes,
        Property.Type.HOTEL: HotelAttributes,
        Property.Type.BASEMENT_PARKING: BasementParkingAttributes,
        Property.Type.GARAGE: GarageAttributes,
        Property.Type.STORAGE_ROOM: StorageRoomAttributes,
        Property.Type.COMPLEX: ComplexAttributes
    }

    try:
        if type in switcher.keys():
            return switcher.get(type)
    except KeyError:
        raise KeyError(
            'Wrong key in property type switcher dictionary (properties.utils.get_attributes_object)'
        )


def client_form_handling(request):
    form = ClientForm(request.POST)
    if form.is_valid():
        client = form.save(commit=False)
        client.user = request.user
        client.office = request.user.office
        client.save()

        last_added_client = [
            Client.objects.all().order_by('-created_at').first().pk,
            Client.objects.all().order_by('-created_at').first().get_display_full_name()
        ]

        return JsonResponse({'last_client': last_added_client})

    errors = {str(key): value[0] for key, value in form.errors.items()}

    return JsonResponse(status=400, data=errors)


def get_property_attributes_filter_queryset(lookup_field, value, is_api_offer_filter=False):
    qs = Q()
    for property_type in Property.Type.values:
        attributes_class = get_attributes_object(property_type)
        if hasattr(attributes_class, lookup_field.split('__')[0]):
            if is_api_offer_filter:
                field = "property__" + "__".join([property_type + '_attributes', lookup_field])
            else:
                field = "__".join([property_type + '_attributes', lookup_field])
            query_dict = {
                field: value
            }

            qs = qs | Q(**query_dict)

    return qs


def get_demands_queryset(property):
    if not property.attributes_object:
        return []

    fields = {
        "property_type": property.type,
        "region": property.region,
        "city": property.city,
        "active": True,
        "type__in": property.offers.exclude(is_closed=True).filter(
            status__in=settings.MATCHED_STATUSES).values_list('type', flat=True)
    }

    if property.zone:
        fields.update({"zones": property.zone})

    qs = Demand.objects.filter(
        **fields
    )

    if getattr(property.attributes_object, 'ground_floor', None):
        qs = qs.exclude(ground_floor_excluded=True)

    if getattr(property.attributes_object, 'top_floor', None):
        qs = qs.exclude(top_floor_excluded=True)

    if getattr(property.attributes_object, 'mansard', None):
        qs = qs.exclude(mansard_excluded=True)

    property_feature_ids = [x['id'] for x in property.features.values('id')]
    for feature in Feature.objects.all():
        if feature.id not in property_feature_ids:
            qs = qs.exclude(features=feature)

    if getattr(property.attributes_object, 'rooms_number', None):
        qs = qs.filter(Q(rooms='') | Q(rooms__icontains=str(property.attributes_object.rooms_number)))

    if settings.CLIENT != 'rmm':
        if getattr(property.attributes_object, 'surface_util', None):
            qs = qs.filter(
                Q(surface_min__lte=property.attributes_object.surface_util,
                  surface_max__gte=property.attributes_object.surface_util) |
                Q(surface_min__lte=property.attributes_object.surface_util, surface_max__isnull=True) |
                Q(surface_min__isnull=True, surface_max__gte=property.attributes_object.surface_util) |
                Q(surface_min__isnull=True, surface_max__isnull=True)
            )

    else:
        if getattr(property.attributes_object, 'surface_total', None):
            qs = qs.filter(
                Q(surface_min__lte=property.attributes_object.surface_total,
                  surface_max__gte=property.attributes_object.surface_total) |
                Q(surface_min__lte=property.attributes_object.surface_total, surface_max__isnull=True) |
                Q(surface_min__isnull=True, surface_max__gte=property.attributes_object.surface_total) |
                Q(surface_min__isnull=True, surface_max__isnull=True)
            )

    if getattr(property.get_last_rent_offer(), 'price', None):
        qs = qs.filter(
            Q(price_min__lte=property.get_last_rent_offer().price,
              price_max__gte=property.get_last_rent_offer().price) |
            Q(price_min__lte=property.get_last_rent_offer().price, price_max__isnull=True) |
            Q(price_min__isnull=True, price_max__gte=property.get_last_rent_offer().price) |
            Q(price_min__isnull=True, price_max__isnull=True)
        )

    if getattr(property.get_last_sale_offer(), 'price', None):
        qs = qs.filter(
            Q(price_min__lte=property.get_last_sale_offer().price,
              price_max__gte=property.get_last_sale_offer().price) |
            Q(price_min__lte=property.get_last_sale_offer().price, price_max__isnull=True) |
            Q(price_min__isnull=True, price_max__gte=property.get_last_sale_offer().price) |
            Q(price_min__isnull=True, price_max__isnull=True)
        )

    return qs.order_by('-created_at').distinct()


def get_properties_queryset(demand):
    fields = {
        'type': demand.property_type,
        'region': demand.region,
        'city': demand.city,
        'offers__type': demand.type,
    }

    if len(demand.zones.values()) > 0:
        fields.update({'zone__in': [x['id'] for x in list(demand.zones.values())]})

    qs = Property.objects.filter(
        **fields
    )

    if getattr(demand, 'mansard_excluded'):
        qs = qs.filter(get_property_attributes_filter_queryset('mansard', not demand.mansard_excluded))

    if getattr(demand, 'ground_floor_excluded'):
        qs = qs.filter(get_property_attributes_filter_queryset('ground_floor', not demand.ground_floor_excluded))

    if getattr(demand, 'top_floor_excluded'):
        qs = qs.filter(get_property_attributes_filter_queryset('top_floor', not demand.top_floor_excluded))

    if getattr(demand, 'new_building'):
        qs = qs.filter(get_property_attributes_filter_queryset('new_building', demand.new_building))

    if getattr(demand, 'in_development'):
        qs = qs.filter(get_property_attributes_filter_queryset('in_development', demand.in_development))

    demand_feature_ids = [x['id'] for x in demand.features.values('id')]
    for feature in Feature.objects.all():
        if feature.id in demand_feature_ids:
            qs = qs.filter(features=feature)

    if settings.CLIENT != 'rmm':
        if getattr(demand, 'surface_min'):
            qs = qs.filter(get_property_attributes_filter_queryset('surface_util__gte', demand.surface_min))

        if getattr(demand, 'surface_max'):
            qs = qs.filter(get_property_attributes_filter_queryset('surface_util__lte', demand.surface_max))

    else:
        if getattr(demand, 'surface_min'):
            qs = qs.filter(get_property_attributes_filter_queryset('surface_total__gte', demand.surface_min))

        if getattr(demand, 'surface_max'):
            qs = qs.filter(get_property_attributes_filter_queryset('surface_total__lte', demand.surface_max))

    if getattr(demand, 'rooms'):
        if '4' in demand.rooms:
            qs = qs.filter(
                get_property_attributes_filter_queryset('rooms_number__gte', min([int(x) for x in demand.rooms])))
        qs = qs.filter(get_property_attributes_filter_queryset('rooms_number__in', [int(x) for x in demand.rooms]))

    if getattr(demand, 'price_min'):
        qs = qs.filter(offers__price__gte=demand.price_min, offers__type=demand.type)

    if getattr(demand, 'price_max'):
        qs = qs.filter(offers__price__lte=demand.price_max, offers__type=demand.type)

    return qs.order_by('offers__status', '-updated_at').distinct()


def status_check(offer):
    if getattr(offer.property, 'attributes_object') and offer.status == settings.STATUS.ACTIVE:
        attributes_object = offer.property.attributes_object

        if attributes_object.description and offer.price:
            return True
        else:
            return False

    return True


def offer_check(post_request):
    post_data = list(post_request.values())

    if post_data.count(settings.STATUS.ACTIVE) == 2 and post_data.count(Offer.ContractType.SALE) == 3:
        return False

    if post_data.count(settings.STATUS.ACTIVE) == 2 and post_data.count(Offer.ContractType.RENT) == 2:
        return False

    return True


def remove_coma(post_request):
    post_request = post_request.copy()
    for key in post_request.keys():
        post_request[key] = post_request[key].replace(',', '')

    return post_request


activities_statuses = [
    Activity.Status.TO_DO,
    Activity.Status.IN_PROGRESS,
    Activity.Status.DONE,
]

leads_statuses = [
    Activity.Status.SALE,
    Activity.Status.RENT,
    Activity.Status.PROCESSED,
]


def get_activities_ids(qs):
    activities_ids = ''
    for activity in qs:
        if getattr(activity, 'property'):
            activities_ids += f'{activity.id}-{"property"}-{activity.property.id}&'
        if getattr(activity, 'client'):
            activities_ids += f'{activity.id}-{"client"}-{activity.client.id}&'
        if getattr(activity, 'demand'):
            activities_ids += f'{activity.id}-{"demand"}-{activity.demand.id}&'

    return activities_ids


def get_activities_context_dict(qs):
    activities_context_dict = {
        'to_do': {
            'title': _('To do'),
            'id': 'task-list-to-do',
            'qs': qs.filter(status=Activity.Status.TO_DO),
            'status': Activity.Status.TO_DO
        },

        'in_progress': {
            'title': _('In progress'),
            'id': 'task-list-in-progress',
            'qs': qs.filter(status=Activity.Status.IN_PROGRESS),
            'status': Activity.Status.IN_PROGRESS
        },

        'done': {
            'title': _('Done'),
            'id': 'task-list-done',
            'qs': qs.filter(status=Activity.Status.DONE),
            'status': Activity.Status.DONE
        }
    }

    return activities_context_dict


def get_leads_context_dict(qs):
    leads_context_dict = {
        'sale_offers': {
            'title': _('Leads generated'),
            'id': 'task-list-sale',
            'qs': qs.filter(status=Activity.Status.SALE),
            'status': Activity.Status.SALE
        },

        'rent_offers': {
            'title': _('Interested leads'),
            'id': 'task-list-rent',
            'qs': qs.filter(status=Activity.Status.RENT),
            'status': Activity.Status.RENT
        },

        'processed': {
            'title': _('Processed leads'),
            'id': 'task-list-processed',
            'qs': qs.filter(status=Activity.Status.PROCESSED),
            'status': Activity.Status.PROCESSED
        }
    }

    return leads_context_dict


def get_coordinates(property):
    street_number = getattr(property, 'street_number', '')
    street = getattr(property, 'street', '')
    city = getattr(property, 'city', '')
    region = getattr(property, 'region', '')
    url = f'{settings.GOOGLE_API_DNS_HOST}?address={street_number}+{street},+{city},+{region}&key={settings.GOOGLE_API_KEY}'
    property_latitude = settings.GEO_COORDINATES_DEFAULT[0]
    property_longitude = settings.GEO_COORDINATES_DEFAULT[1]

    try:
        geo_coordinates = requests.get(url).json()
    except Exception as e:
        print(f'Google maps api call failed: {e}')
    else:
        if 'results' in geo_coordinates and geo_coordinates['results']:
            property_latitude = geo_coordinates['results'][0]['geometry']['location']['lat']
            property_longitude = geo_coordinates['results'][0]['geometry']['location']['lng']

    return property_latitude, property_longitude


class UserHasPermissions(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user or \
               self.request.user.is_superuser or \
               self.request.user.groups.filter(name__in=['Office Managers', 'Region Managers']).exists() and \
               self.request.user.office == self.request.user.office


class UserIsManager(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_manager and self.request.user.is_staff


class UserCanCreateAgent(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or \
               self.request.user.groups.filter(name__in=['Office Managers', 'Region Managers']).exists()


sort_values = (
    ('', _('Sort by...')),
    ("created_at", _('Created At Asc')),
    ("-created_at", _('Created At Des')),
    ("updated_at", _('Updated At Asc')),
    ("-updated_at", _('Updated At Des')),
)



def get_number_of_activites(list_activities):
    dict_activ = {}
    for activity in list_activities:
        if activity.get_type_display() in dict_activ:
            dict_activ[activity.get_type_display()]+=1
        else:
            dict_activ[activity.get_type_display()] = 1
    return dict_activ
