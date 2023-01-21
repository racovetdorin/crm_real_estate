import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver

from audit.models import AuditableModel, ModelDiffMixin
from clients.models import Client
from crm.models import SoftDeleteModel, ImageModel, DocumentModel
from locations.models import Street, Zone, City, Region
from offices.models import Office
from users.models import User
from django.apps import apps


class Property(AuditableModel, SoftDeleteModel):
    class Type(models.TextChoices):
        HOUSE = 'house', _('House')
        APARTMENT = 'apartment', _('Apartment')
        STUDIO = 'studio', _('Studio')
        COMMERCIAL = 'commercial', _('Commercial space')
        LAND = 'land', _('Land')
        HOTEL = 'hotel', _('Hotel')
        CABIN = 'cabin', _('Cabin')
        COMPLEX = 'complex', _('Complex')
        BASEMENT_PARKING = 'basement_parking', _('Basement Parking')
        GARAGE = 'garage', _('Garage') 
        STORAGE_ROOM = 'storage_room', _('Storage Room') 

    class Floor(models.TextChoices):
        BASEMENT = 'basement', _('Basement')
        SEMI_BASEMENT = 'semi_basement', _('Semi Basement')
        GROUND_FLOOR = 'ground_floor', _('Ground Floor')
        ENTRESOL_FLOOR = 'entresol_floor', _('Entresol')
        MANSARD = 'mansard', _('Mansard')
        ONE = '1', '1'
        TWO = '2', '2'
        THREE = '3', '3'
        FOUR = '4', '4'
        FIVE = '5', '5'
        SIX = '6', '6'
        SEVEN = '7', '7'
        EIGHT = '8', '8'
        NINE = '9', '9'
        TEN = '10', '10'
        ELEVEN = '11', '11'
        TWELVE = '12', '12'
        THIRTEEN = '13', '13'
        FOURTEEN = '14', '14'
        FIFTEEN = '15', '15'
        SIXTEEN = '16', '16'
        SEVENTEEN = '17', '17'
        EIGHTEEN = '18', '18'
        NINETEEN = '19', '19'
        TWENTY = '20', '20'

    type = models.CharField(db_index=True, max_length=56, choices=Type.choices, blank=True, null=True,
                            verbose_name=_('Type'))

    user = models.ForeignKey(User, db_index=True, null=True, related_name="properties", on_delete=models.SET_NULL,
                             verbose_name=_('Agent'))
    office = models.ForeignKey(Office, db_index=True, null=True, related_name="properties", on_delete=models.SET_NULL,
                               verbose_name=_('Office'))

    client = models.ForeignKey(Client, null=True, blank=True, related_name="properties", on_delete=models.SET_NULL,
                               verbose_name=_('Client'))
    recommendation = models.TextField(blank=True, null=True, verbose_name=_('Recommendation'))  

    conclusion = models.TextField(blank=True, null=True, verbose_name=_('Conclusion'))

    features = models.ManyToManyField("properties.Feature", blank=True, verbose_name=_('Features'))

    attributes_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    attributes_object_id = models.PositiveIntegerField(null=True)
    attributes_object = GenericForeignKey('attributes_type', 'attributes_object_id')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    report_start_date = models.DateField(null=True, blank=True, verbose_name=_('Report start date'))
    report_end_date = models.DateField(null=True, blank=True, verbose_name=_('Report end date'))

    region = models.ForeignKey(Region, blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name=_(u'Region'))
    city = models.ForeignKey(City, blank=True, null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=_(u'City'))
    zone = models.ForeignKey(Zone, blank=True, null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=_(u'Zone'))
    street = models.ForeignKey(Street, blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name=_(u'Street'))

    virtual_tour = models.CharField(max_length=1000, blank=True, verbose_name=_('Virtual tour'), default='')
    video_tour = models.CharField(max_length=1000, blank=True, verbose_name=_('Video tour'), default='')

    street_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Street number'))
    block_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Block number'))
    block_entrance_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Block entrance'))
    floor = models.CharField(max_length=20, null=True, blank=True, choices=Floor.choices, verbose_name=_('Floor'))
    apartment_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Ap. number'))

    latitude = models.FloatField(blank=True, null=True, verbose_name=_('Latitude'),
                                 default=settings.GEO_COORDINATES_DEFAULT[0])
    longitude = models.FloatField(blank=True, null=True, verbose_name=_('Longitude'),
                                  default=settings.GEO_COORDINATES_DEFAULT[1])

    demands_of_interest = models.ManyToManyField('demands.Demand', blank=True, verbose_name=_('Demands of interest'))

    complex = models.ForeignKey('Property', blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name=_(u'Complex'))
    external_id = models.CharField(max_length=50, default=uuid.uuid4, verbose_name=_(u'Property External ID'))
    
    class Meta:
        unique_together = (
            ['attributes_type', 'attributes_object_id']
        )

    def __str__(self):
        try:
            return '{} {}'.format(self.id, self.complex_attributes.first().description_sentimental)
        except:
            return '{} {}'.format(self.id, _(self.get_display_object_class()))

    @property
    def public_images(self):
        return self.images.filter(hide_on_site=False)

    @property
    def thumbnail(self):
        return self.images.filter(hide_on_site=False).first()

    def get_absolute_url(self):
        if self.attributes_object and not self.complex:
            return reverse(settings.ALL_PROPERTIES_LIST_ROUTE)

        else:
            return reverse(settings.PROPERTIES_UPDATE_ROUTE, args=[self.id])

    def get_display_title(self):
        return self.Type(self.type).label

    def get_display_type(self):
        return self.Type(self.type).label

    def get_display_city(self):
        if self.city:
            return self.city.name

    def get_display_zone(self):
        if self.city:
            return self.zone.name

    def get_last_rent_offer(self):
        from offers.models import Offer
        return self.offers.filter(type=Offer.ContractType.RENT, is_closed=False).order_by('-created_at').first() or None

    def get_last_sale_offer(self):
        from offers.models import Offer
        return self.offers.filter(type=Offer.ContractType.SALE, is_closed=False).order_by('-created_at').first() or None

    def get_last_offers(self):
        return self.offers.filter(is_closed=False).order_by('created_at')

    def get_thumbnail_url(self):
        try:
            return self.images.filter(property_id=self.id).order_by('position').first().image_path
        except AttributeError:
            return None

    def get_full_thumbnail_url(self):
        if self.get_thumbnail_url():
            return settings.CDN_MEDIA_URL + self.get_thumbnail_url()

        return ''

    def get_display_object_class(self):
        return self.__class__.__name__

    def is_exclusive(self):
        for offer in self.get_last_offers():
            if offer.exclusive:
                return True

        return False

    def get_display_role(self):
        try:
            return settings.ROLES(self.role).label
        except ValueError:
            pass

    def get_list_background_color_code(self):
        BLUE = '#B6DCDF'
        RED = '#FDCECE'
        WHITE = '#FFFFFF'
        YELLOW = '#FDF3CE'

        from offers.models import Offer
        if not self.get_last_offers():
            return WHITE

        for offer in self.get_last_offers():
            if offer.status == settings.STATUS.ACTIVE and offer.promote_site:
                return BLUE

        for offer in self.get_last_offers():
            if offer.status == settings.STATUS.ACTIVE and not offer.promote_site:
                return YELLOW

        for offer in self.get_last_offers():
            if offer.status == settings.STATUS.INCOMPLETE and not offer.promote_site:
                return WHITE

        return RED

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
        Property.Type.COMPLEX: ComplexAttributes,
    }

    try:
        if type in switcher.keys():
            return switcher.get(type)
        else:
            return None
    except KeyError:
        raise KeyError(
            'Wrong key in property type switcher dictionary (properties.utils.get_attributes_object)'
        )

# method for updating
@receiver(post_save, sender=Property)
def post_save(sender, instance, created, **kwargs):
    if created and instance.complex:
        if not instance.office and instance.complex.office:
            instance.office = instance.complex.office

        if not instance.region and instance.complex.region:
            instance.region = instance.complex.region

        if not instance.city and instance.complex.city:
            instance.city = instance.complex.city

        if not instance.zone and instance.complex.zone:
            instance.zone = instance.complex.zone

        if not instance.street and instance.complex.street:
            instance.street = instance.complex.street

        if not instance.virtual_tour and instance.complex.virtual_tour:
            instance.virtual_tour = instance.complex.virtual_tour

        if not instance.video_tour and instance.complex.video_tour:
            instance.video_tour = instance.complex.video_tour

        if not instance.street_number and instance.complex.street_number:
            instance.street_number = instance.complex.street_number

        if not instance.block_number and instance.complex.block_number:
            instance.block_number = instance.complex.block_number

        if not instance.block_entrance_number and instance.complex.block_entrance_number:
            instance.block_entrance_number = instance.complex.block_entrance_number

        if not instance.floor and instance.complex.floor:
            instance.floor = instance.complex.floor

        if not instance.apartment_number and instance.complex.apartment_number:
            instance.apartment_number = instance.complex.apartment_number

        if not instance.latitude and instance.complex.latitude:
            instance.latitude = instance.complex.latitude

        if not instance.longitude and instance.complex.longitude:
            instance.longitude = instance.complex.longitude

        
        for feature in instance.complex.features.all():
            if not instance.features.filter(name=feature.name).exists():
                instance.features.add(feature)

        property_documents = PropertyDocument.objects.filter(property=instance, deleted=False)
        if len(property_documents) == 0:
            complex_documents = PropertyDocument.objects.filter(property=instance.complex, deleted=False)
            if len(complex_documents) > 0:
                for document in complex_documents:
                    document.pk = None
                    document.property = instance
                    document.save()
        
        property_images = PropertyImage.objects.filter(property=instance, deleted=False)
        if len(property_images) == 0:
            complex_images = PropertyImage.objects.filter(property=instance.complex, deleted=False)
            if len(complex_images) > 0:
                for image in complex_images:
                    image.pk = None
                    image.property = instance
                    image.save()
        complex_attribute = instance.complex.complex_attributes.first()
        if complex_attribute:
            property_attributes_class = get_attributes_object(instance.Type(instance.type).value)
            property_attribute, created = property_attributes_class.objects.get_or_create(property__in=[instance])
            if created:
                attrs_list = [
                    'top_floor', 'ground_floor', 'mansard', 'new_building', 'in_development', 'key_holding', 'partitioning', 'comfort', 'orientation',
                    'energy_class', 'construction_year', 'built', 'interior_state', 'construction_material', 'floors', 'rooms_number', 'bathrooms_number', 
                    'kitchens_number', 'balconies_number', 'internet_connection', 'garage', 'furnished', 'windows', 'heating_source', 'cadastral_number', 
                    'topographic_number', 'land_registry', 'description', 'description_private', 'description_sentimental', 'surface_total', 'surface_util',
                    'surface_built', 'surface_field', 'surface_garden', 'front_line'
                ]

                # property_attribute.top_floor = complex_attribute.top_floor
                for attr in attrs_list:
                    if getattr(complex_attribute, attr):
                        setattr(property_attribute, attr, getattr(complex_attribute, attr))
                # property_attribute.top_floor = True
                property_attribute.property.add(instance)
                property_attribute.save()

class FeatureGroup(models.Model):
    display_name = models.CharField(max_length=200, verbose_name=_('Display name'))
    slug = models.SlugField(max_length=200)
    property_type = MultiSelectField(max_length=200, null=True, blank=True, choices=Property.Type.choices,
                                     verbose_name=_('Property type'))

    def __str__(self):
        return self.display_name

    def get_display_property_type(self):
        return Property.Type(self.property_type).label


class Feature(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    group = models.ForeignKey(FeatureGroup, related_name="features", on_delete=models.CASCADE, verbose_name=_('Group'))
    is_filtered = models.BooleanField(default=False, verbose_name=_('Is filtered'))

    def __str__(self):
        return "{} - {}".format(self.name, self.group.slug)


class BasePropertyAttributes(ModelDiffMixin, models.Model):

    class UnitsOfMeasure(models.TextChoices):
        SQUARE_METERS = 'square_meters', _('Square meters')
        ACRES = 'acres', _('Acres')
        HECTARES = 'hectares', _('Hectares')

    title = models.CharField(max_length=70, blank=True, null=True,
                             verbose_name=_('Title'))  # deprecated - should not be used anymore, use description_sentimental instead
    description = models.TextField(max_length=3000, blank=True, null=True, verbose_name=_('Description public'))
    description_english = models.TextField(max_length=3000, blank=True, null=True,
                                           verbose_name=_('Description in english'))
    
    description_private = models.TextField(max_length=3000, blank=True, null=True,
                                           verbose_name=_('Description private'))
    
    description_sentimental = models.CharField(max_length=256, null=True, blank=True,
                                               verbose_name=_('Description sentimental'))
    

    surface_total = models.FloatField(null=True, blank=True, verbose_name=_('Surface total'))
    surface_util = models.FloatField(blank=True, null=True, verbose_name=_('Surface util'))
    surface_built = models.FloatField(blank=True, null=True, verbose_name=_('Surface built'))
    surface_field = models.FloatField(blank=True, null=True, verbose_name=_('Surface field'))
    surface_garden = models.FloatField(blank=True, null=True, verbose_name=_('Surface garden'))
    surface_kitchen = models.FloatField(blank=True, null=True, verbose_name=_('Surface kitchen'))
    front_line = models.FloatField(blank=True, null=True, verbose_name=_('Front line'))
    ceiling_height = models.FloatField(blank=True, null=True, verbose_name=_('Ceiling height'))

    units_of_measure = models.CharField(max_length=50, blank=True, null=True, choices=UnitsOfMeasure.choices,
                                        default=UnitsOfMeasure.SQUARE_METERS,
                                        verbose_name=_('Units of measure'),
                                        )

    class Meta:
        abstract = True

    def get_title_prefix(self):
        return f"Proprietate"


class BaseConstructionAttributes(BasePropertyAttributes):
    class Partitioning(models.TextChoices):
        OPEN_SPACE = 'open-space', _('Open-space')
        CIRCUIT = 'circuit', _('Circuit')
        SEMI_DETACHED = 'semidetached', _('Semi-detached')
        DETACHED = 'detached', _('Detached')
        WAGON = 'wagon', _('Wagon')

    class Comfort(models.TextChoices):
        ENHANCED = 'increased', _('Increased')
        ONE = 'one', _('One')
        UNIQUE = 'unique', _('Unique')
        TWO = 'two', _('Two')
        THREE = 'three', _('Three')

    class Orientation(models.TextChoices):
        NORTH = 'north', _('North')
        NORTHEAST = 'northeast', _('Northeast')
        EAST = 'east', _('East')
        SOUTHEAST = 'southeast', _('Southeast')
        SOUTH = 'south', _('South')
        SOUTHWEST = 'southwest', _('Southwest')
        WEST = 'west', _('West')
        NORTHWEST = 'northwest', _('Northwest')
        NORTHSOUTH = 'northsouth', _('Northsouth')
        EASTWEST = 'eastwest', _('Eastwest')

    class HeatingSource(models.TextChoices):
        CENTRAL_HEATING_BUILDING = 'central_heating', _('Central heating in building')
        INDIVIDUAL_CENTRAL_HEATING = 'individual_central_heating', _('Individual central heating')
        UNDERFLOOR_HEATING = 'underfloor_heating', _('Underfloor heating')
        DISTRICT_HEATING = 'district_heating', _('District heating')
        WOOD_CENTRAL_HEATING = 'wood_central_heating', _('Wood central heating')
        FIREPLACE = 'fireplace', _('Fireplace')
        CONVECTORS = 'convectors', _('Convectors')

    class EnergyEfficiency(models.TextChoices):
        A = 'a', 'A'
        B = 'b', 'B'
        C = 'c', 'C'
        D = 'd', 'D'
        E = 'e', 'E'
        F = 'f', 'F'
        G = 'g', 'G'

    class InternetConnection(models.TextChoices):
        FIBER_OPTICS = 'fiber_optics', _('Fiber optics')
        CABLE = 'cable', _('Cable')

    class AllowChildrens(models.TextChoices):
        CHILDREN_ARE_ACCEPTED = 'children_are_accepted', _('Children are accepted')
        WITHOUT_CHILDREN = 'without_children', _('Without children')

    class AllowAnimals(models.TextChoices):
        ANIMALS_ARE_ACCEPTED = 'animals_are_accepted', _('Animals are accepted')
        WITHOUT_ANIMALS = 'without_animals', _('Without animals')

    class GarageType(models.TextChoices):
        GARAGE = 'garage', _('Garage')
        UNDERGROUND_GARAGE = 'underground_garage', _('Underground parking')
        EXTERIOR_PARKING = 'exterior_parking', _('Exterior parking')
        SUBSCRIPTION_PARKING = 'subscription_parking', _('Subscription parking')

    class Furnished(models.TextChoices):
        SEMI_FURNISHED = 'semi_furnished', _('Semi-furnished')
        FURNISHED_KITCHEN = 'furnished_kitchen', _('Furnished kitchen')
        FURNISHED_MODERN = 'furnished_modern', _('Furnished with modern utilities')
        FURNISHED_CLASSIC = 'furnished_classic', _('Furnished with classic utilities')
        LUX = 'lux', _('Luxurious')

    class WindowsType(models.TextChoices):
        DOUBLE_GLAZING = 'double_glazing', _('Double glazing glass')
        WOOD_GLASS = 'wood_glass', _('Wood and glass')

    top_floor = models.BooleanField(default=False, verbose_name=_('Is top floor'))
    ground_floor = models.BooleanField(default=False, verbose_name=_('Is ground floor'))
    mansard = models.BooleanField(default=False, verbose_name=_('Is mansard'))
    new_building = models.BooleanField(default=False, verbose_name=_('New building'))
    in_development = models.BooleanField(default=False, verbose_name=_('In development'))
    key_holding = models.BooleanField(default=False, verbose_name=_('Key holding'))

    partitioning = models.CharField(max_length=50, null=True, choices=Partitioning.choices, blank=True,
                                    verbose_name=_('Partitioning'))
    comfort = models.CharField(max_length=50, null=True, choices=Comfort.choices, blank=True, verbose_name=_('Comfort'))
    orientation = models.CharField(max_length=50, null=True, choices=Orientation.choices, blank=True,
                                   verbose_name=_('Orientation'))
    energy_class = models.CharField(max_length=20, choices=EnergyEfficiency.choices, blank=True, null=True,
                                    verbose_name=_('Energy class'))
    construction_year = models.IntegerField(null=True, blank=True, verbose_name=_('Construction year'))
    built = models.CharField(max_length=256, null=True, blank=True, choices=settings.BUILT_PERIOD.choices,
                             verbose_name=_('Built'))
    interior_state = models.CharField(max_length=50, null=True, choices=settings.INTERIOR_STATE.choices, blank=True,
                                      verbose_name=_('Interior state'))
    construction_material = models.CharField(max_length=50, null=True, choices=settings.CONSTRUCTION_MATERIALS.choices,
                                             blank=True, verbose_name=_('Construction material'))
    floors = models.IntegerField(null=True, choices=((x, x) for x in range(0, 21)), blank=True,
                                 verbose_name=_('Total Floors'))

    rooms_number = models.IntegerField(null=True, choices=((x, x) for x in range(1, 21)), blank=True,
                                       verbose_name=_('Rooms number'))
    
    bathrooms_number = models.IntegerField(null=True, choices=((x, x) for x in range(1, 11)), blank=True,
                                           verbose_name=_('Bathrooms number'))
    kitchens_number = models.IntegerField(null=True, choices=((x, x) for x in range(1, 6)), blank=True,
                                          verbose_name=_('Kitchens number'))
    balconies_number = models.IntegerField(null=True, choices=((x, x) for x in range(1, 11)), blank=True,
                                           verbose_name=_('Balconies number'))
    internet_connection = models.CharField(max_length=256, choices=InternetConnection.choices, blank=True, null=True,
                                           verbose_name=_('Internet connection'))
    garage = models.CharField(max_length=256, choices=GarageType.choices, blank=True, null=True,
                              verbose_name=_('Parking'))
    furnished = models.CharField(max_length=256, choices=Furnished.choices, blank=True, null=True,
                                 verbose_name=_('Furnished'))
    windows = models.CharField(max_length=256, choices=WindowsType.choices, blank=True, null=True,
                               verbose_name=_('Windows'))
    heating_source = models.CharField(max_length=256, choices=HeatingSource.choices, null=True, blank=True,
                                      verbose_name=_('Heating source'))
    allow_childrens = models.CharField(max_length=256, choices=AllowChildrens.choices, null=True, blank=True,
                                      verbose_name=_('Allow Childrens'))
    allow_animals = models.CharField(max_length=256, choices=AllowAnimals.choices, null=True, blank=True,
                                      verbose_name=_('Allow Animals'))
    cadastral_number = models.CharField(max_length=50, blank=True, default='', verbose_name=_('Cadastral number'))

    topographic_number = models.CharField(max_length=50, blank=True, default='', verbose_name=_('Topographic number'))

    land_registry = models.CharField(max_length=50, blank=True, default='', verbose_name=_('Land registry'))

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='construction_attr')
    

    class Meta:
        abstract = True


class HouseAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        DETACHED = 'detached', _('Detached house')
        TERRACED = 'terraced', _('Terraced house')
        ATTACHED = 'attached', _('Attached house')
    
    class House_state(models.TextChoices):
        INDIVIDUAL_DESIGN = 'individual_design', _('Individual design')
        WITHOUT_REPARATION = 'without_reparation', _('Without reparation')
        DEMOLITION_HOUSE = 'demolition_house', _('Demolition House')
        UNFINISHED_CONSTRUCTION = 'unfinished_construction', _('Unfinished Construction')
        NEED_REPARATION = 'need_reparation', _('Need Reparation')
        IN_GREY = 'in_grey', _('In grey')
        IN_WHITE = 'in_white', _('In white')
        COSMETIC_REPARATION = 'cosmetic_reparation', _('Cosmetic Reparation')
        EURO_REPARATION = 'euro_reparation', _('Euro reparation')
        READY_FOR_USE = 'ready_for_use', _('Ready for use')

    class House_construction_material(models.TextChoices):
        PANELS = 'panels', _('Panels')
        LIMESTONE = 'limestone', _('Limestone')
        BRICK = 'brick', _('Brick')
        BLOCKS = 'blocks', _('Blocks')
        MONOLITH = 'monolith', _('Monolith')
        CONCRETE = 'concrete', _('Concrete')
        COMBINED = 'combined', _('Combined')
        BCA = 'bca', _('BCA')
        WOOD = 'wood', _('Wood')
        OTHER = 'other', _('Other')
        
    class Sewerage(models.TextChoices):
        WITHOUT_SEWERAGE = 'without_sewerage', _('Without sewerage')
        THERE_SEWER = 'there_sewer', _('There is a sewer')
        
    class Water_pipes(models.TextChoices):        
        WITHOUT_PLUMBING = 'without_plumbing', _('Without plumbing')
        THERE_RUNNING_WATER = 'there_running_water', _('There is running water')
    
    class Gasification(models.TextChoices):
        GASIFIED = 'gasified', _('Gasified')
        NOT_GASIFIED = 'not_gasified', _('Not gasified')
        

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='house_attributes')
    subtype = models.CharField(max_length=50, null=True, choices=Subtype.choices, default=Subtype.DETACHED, blank=True,
                               verbose_name=_('House subtype'))
    house_state = models.CharField(max_length=30, null=True, blank=True, choices=House_state.choices, verbose_name=_('House State'))
    
    house_construction_material = models.CharField(max_length=30, null=True, blank=True, choices=House_construction_material.choices, verbose_name=_('Construction material'))
    
    sewerage = models.CharField(max_length=50, null=True, blank=True, choices=Sewerage.choices,
                                            verbose_name=_('Sewerage'))
    
    water_pipes = models.CharField(max_length=50, null=True, blank=True, choices=Water_pipes.choices,
                                            verbose_name=_('Water pipes'))
    
    gasification = models.CharField(max_length=50, null=True, blank=True, choices=Gasification.choices,
                                            verbose_name=_('Gasification'))

    def get_title_prefix(self):
        return f"Casă cu {self.rooms_number} camere"


class ApartmentAttributes(BaseConstructionAttributes):

    class Subtype(models.TextChoices):
        BLOCK_APARTMENT = 'block_apartment', _('Block apartment')
        VILLA_APARTMENT = 'villa_apartment', _('Villa apartment')

    class Building_plan(models.TextChoices):
        a102 = '102', _('102')
        a135 = '135', _('135')
        a143 = '143', _('143')
        Gostinca = 'gostinca', _('Ap. "Gostinka"')
        Brejnevka = 'brejnevka', _('Brj (Brejnevka)')
        Camin_familial = 'camin_familial', _('Cămin familial')
        Ceska = 'ceska', _('Cş (Ceşka)')
        Hrusciovka = 'hrusciovka', _('Hruşciovka')
        Individuala = 'individuala', _('Individuală')
        Ms_serie_moldovenească = 'ms_serie_moldoveneasca', _('Ms (serie  moldovenească)')
        Pe_pamant = 'pe_pamant', _('Pe pămănt')
        Rubaska = 'rubaska', _('Rubaşka')
        Stalinka = 'stalinka', _('St (Stalinka)')
        Vart = 'vart', _('Varț (Varnițkaia)')

    class Apartment_state(models.TextChoices):
        IN_WHITE = 'in_white', _('In white')
        IN_GREY = 'in_grey', _('In grey')
        EURO_REPARATION = 'euro_reparation', _('Euro reparation')
        INDIVIDUAL_DESIGN = 'individual_design', _('Individual design')
        WITHOUT_REPARATION = 'without_reparation', _('Without reparation')
        READY_FOR_USE = 'ready_for_use', _('Ready for use')
        UNFINISHED_CONSTRUCTION = 'unfinished_construction', _('Unfinished Construction')
        NEED_REPARATION = 'need_reparation', _('Need Reparation')
        COSMETIC_REPARATION = 'cosmetic_reparation', _('Cosmetic Reparation')
        DEMOLITION_HOUSE = 'demolition_house', _('Demolition House')

    class Apartment_construction_material(models.TextChoices):
        CONCRETE = 'concrete', _('Concrete')
        BCA = 'bca', _('BCA')
        BLOCKS = 'blocks', _('Blocks')
        COMBINED = 'combined', _('Combined')
        LIMESTONE = 'limestone', _('Limestone')
        BRICK = 'brick', _('Brick')
        WOOD = 'wood', _('Wood')
        MONOLITH = 'monolith', _('Monolith')
        PANELS = 'panels', _('Panels')

    class Rental_fund(models.TextChoices):
        new_construction = 'new_construction', _('Construcţii noi')
        secondary = 'secondary', _('Secundar')

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='apartment_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices,
                               default=Subtype.BLOCK_APARTMENT,
                               verbose_name=_('Apartment subtype'))
    building_plan = models.CharField(max_length=30, null=True, blank=True, choices=Building_plan.choices, verbose_name=_('Building Plan'))
    rental_fund = models.CharField(max_length=20, null=True, blank=True, choices=Rental_fund.choices, verbose_name=_('Rental Fund'))  
    apartment_state = models.CharField(max_length=30, null=True, blank=True, choices=Apartment_state.choices, verbose_name=_('Apartment State'))  
    apartment_construction_material = models.CharField(max_length=30, null=True, blank=True, choices=Apartment_construction_material.choices, verbose_name=_('Construction material'))

    def get_title_prefix(self):
        return f"Apartament cu {self.rooms_number} camere"


class StudioAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        STUDIO_APARTMENT = 'studio_apartment', _('Studio apartment')

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='studio_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices,
                               default=Subtype.STUDIO_APARTMENT,
                               verbose_name=_('Studio subtype'))

    def get_title_prefix(self):
        return f"Garsonieră"


class CommercialAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        COMMERCIAL_SPACE = 'commercial_space', _('Commercial space')
        OFFICE_SPACE = 'office_space', _('Office space')
        INDUSTRIAL_SPACE = 'industrial_space', _('Industrial space')

    class Commercial_state(models.TextChoices):
        INDIVIDUAL_DESIGN = 'individual_design', _('Individual design')
        EURO_REPARATION = 'euro_reparation', _('Euro reparation')
        WITHOUT_REPARATION = 'without_reparation', _('Without reparation')
        IN_WHITE = 'in_white', _('In white')
        IN_GREY = 'in_grey', _('In grey')
        NEED_REPARATION = 'need_reparation', _('Need Reparation')
        COSMETIC_REPARATION = 'cosmetic_reparation', _('Cosmetic Reparation')


    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='commercial_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices,
                               default=Subtype.COMMERCIAL_SPACE,
                               verbose_name=_('Commercial subtype'))
    window_shop = models.BooleanField(default=False, verbose_name=_('Window shop'))

    commercial_state = models.CharField(max_length=30, null=True, blank=True, choices=Commercial_state.choices, verbose_name=_('Commercial State')) 

    def get_title_prefix(self):
        return f"Spațiu comercial"


class LandAttributes(BasePropertyAttributes):
    class Subtype(models.TextChoices):
        AGRICULTURAL_LAND = 'agricultural_land', _('Agricultural land')
        CONSTRUCTION_LAND = 'construction_land', _('Construction land')


    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='land_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices,
                               default=Subtype.AGRICULTURAL_LAND,
                               verbose_name=_('Land subtype'))
                         

    def get_title_prefix(self):
        return f"Teren"


class HotelAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        HOTEL = 'hotel', _('Hotel')
        GUEST_HOUSE = 'guest_house', _('Guest house')

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='hotel_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices, default=Subtype.HOTEL,
                               verbose_name=_('Hotel subtype'))

    def get_title_prefix(self):
        return f"Pensiune"


class CabinAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        CABIN = 'cabin', _('Cabin')

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='cabin_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices, default=Subtype.CABIN,
                               verbose_name=_('Cabin subtype'))

    def get_title_prefix(self):
        return f"Cabană"

class ComplexAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        COMPLEX = 'complex', _('Complex')

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='complex_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices, default=Subtype.COMPLEX,
                               verbose_name=_('Complex subtype'))

    def get_title_prefix(self):
        return f"Ansamblu rezidential"


class GarageAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        GARAGE = 'garage', _('Garage')
    
    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='garage_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices, default=Subtype.GARAGE,
                               verbose_name=_('Garage subtype'))
            
    def get_title_prefix(self):
        return f"Garaj"


class BasementParkingAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        BASEMENT_PARKING = 'basement_parking', _('Basement Parking')

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='basement_parking_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices, default=Subtype.BASEMENT_PARKING,
                               verbose_name=_('Basement Parking subtype'))

    def get_title_prefix(self):
        return f"Parcare Subterană"


class StorageRoomAttributes(BaseConstructionAttributes):
    class Subtype(models.TextChoices):
        STORAGE_ROOM = 'storage_room', _('Storage Room')

    property = GenericRelation(Property, object_id_field='attributes_object_id', content_type_field='attributes_type',
                               related_query_name='storage_room_attributes')
    subtype = models.CharField(max_length=50, blank=True, null=True, choices=Subtype.choices, default=Subtype.STORAGE_ROOM,
                               verbose_name=_('Storage Room subtype'))

    def get_title_prefix(self):
        return f"Debara"


def image_upload_path(instance, filename):
    """
    Returns a custom path to save the property image.
    Includes item id in the path in order to avoid conflicts.
    """
    pass


class PropertyImage(ImageModel):
    property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE, verbose_name=_('Property'))
    rex_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Rex Image ID'),)
    rex_ids = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return 'Image for property with id: {}'.format(self.property.id)


class PropertyDocument(DocumentModel):
    property = models.ForeignKey(Property, related_name="documents", on_delete=models.CASCADE,
                                 verbose_name=_('Property'))

    def __str__(self):
        return 'Document for property with id: {}'.format(self.property.id)


PROPERTY_SUBTYPE_CHOICES = HouseAttributes.Subtype.choices + ApartmentAttributes.Subtype.choices + \
                           StudioAttributes.Subtype.choices + CommercialAttributes.Subtype.choices + \
                           LandAttributes.Subtype.choices + CabinAttributes.Subtype.choices + \
                           HotelAttributes.Subtype.choices + GarageAttributes.Subtype.choices + \
                           StorageRoomAttributes.Subtype.choices + BasementParkingAttributes.Subtype.choices + \
                           ComplexAttributes.Subtype.choices
