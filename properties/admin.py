from re import search
from django.contrib import admin

from offers.models import Offer
from properties.models import *
from django.db.models import Q
from integrations.publisher_remax_global import REXPropertiesHandlerAPI
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

import uuid


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1
class FeatureGroupAdmin(admin.ModelAdmin):
    model = FeatureGroup
    inlines = [FeatureInline]


class PropertyOfferFilter(admin.SimpleListFilter):
    title = "Offer filter for global"
    parameter_name = "data_offer"

    def lookups(self, request, model_admin):
        return (
            ('all', _('All properties')),
            ('offer', _('Active offers for global'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() == 'offer':
            return queryset.filter(Q(offers__promote_site=True) & Q(offers__mls_remax_global=True)).distinct()


api_property_global = REXPropertiesHandlerAPI()

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'user', 'office',
                    'client','city'
                    ]
    list_filter = (PropertyOfferFilter,'user','office')
    actions = ['create_property_admin', 'update_property_admin', 'cancel_listing_admin',
               'cancel_listing_using_externalID_admin', 'delete_images_property_admin', 'get_all_properties_admin',
               'modify_listed_properies_admin', 'migrate_external_id_from_image_to_json_admin',
               'migrate_external_id_from_property_to_offer_admin', 'generate_uuid_admin',
               ]
    search_fields = ('external_id', )

    def create_property_admin(self, request, queryset):
        """
        Action that promotes a queryset of properties to global
        """
        for prop in queryset:
            offers = Offer.objects.filter(property=prop)
            for offer in offers:
                if api_property_global.is_valid_offer(offer) is True and offer.is_closed is False:
                    response = api_property_global.create_property(prop, offer)
                    if response[0] is None and response[1] is None and response[2] is None and response[3] is None:
                        self.message_user(request, _(f"Invalid offer for property: {prop}"))
                        break
                    if not (200 <= response[0].status_code < 300):
                        self.message_user(request, _(f"Error while creating property: {prop}"))
                        offer.mls_remax_global_data['is_created'] = False
                        offer.save()
                        break
                    if not (200 <= response[1].status_code < 300):
                        self.message_user(request, _(f"Error while creating description of {prop}"))
                        offer.mls_remax_global_data['is_created'] = False
                        offer.save()
                        break
                    if response[2] is not None:
                        if not (200 <= response[2].status_code < 300):
                            offer.mls_remax_global_data['is_created'] = False
                            offer.save()
                            self.message_user(request, _(f"Error while creating description in ENG of {prop}"))
                            break
                    offer.mls_remax_global_data = response[0].json()
                    offer.mls_remax_global_data['is_created'] = True
                    offer.save()

        self.message_user(request, _("Properties have been successfully created!"), messages.SUCCESS)

    def update_property_admin(self, request, queryset):
        for prop in queryset:
            offers = Offer.objects.filter(property=prop)
            for offer in offers:
                if api_property_global.is_valid_offer(offer) is True and offer.is_closed is False:
                    response = api_property_global.update_property(prop, offer)
                    if response[0] is None and response[1] is None and response[2] is None and response[3] is None:
                        self.message_user(request, _(f"Invalid offer for property: {prop}"))
                        break
                    if not (200 <= response[0].status_code < 300):
                        self.message_user(request, _(f"Error while updating property: {prop}"))
                        break
                    # Property response json
                    if not (200 <= response[1].status_code < 300):
                        self.message_user(request, _(f"Error while updating description of {prop}"))
                        break
                    # Property eng description update response json
                    if response[2] is not None:
                        if not (200 <= response[2].status_code < 300):
                            self.message_user(request, _(f"Error while updating description in ENG of {prop}"))
                            break
                    offer.mls_remax_global_data = response[0].json()
                    offer.mls_remax_global_data['is_created'] = True
                    if offer.status in ['transacted', 'transacted_by_others',
                            'transacted_by_owner'] and offer.closing_date is not None:
                        offer.mls_remax_global_data['is_transacted'] = True
                    offer.save()

        self.message_user(request, _("Properties have been successfully updated!"), messages.SUCCESS)

    def cancel_listing_admin(self, request, queryset):
        for prop in queryset:
            offers = Offer.objects.filter(property=prop)
            for offer in offers:
                response = api_property_global.cancel_listing(offer, property=prop)
                if not (200 <= response.status_code < 300):
                    self.message_user(request, _(f"Error while deleting property: {prop}"))
                    break
        self.message_user(request, _("Properties have been successfully removed from Global!"), messages.SUCCESS)
    
    def generate_uuid_admin(self, request, queryset):
        for property in queryset:
            offers = Offer.objects.filter(property=property)
            for offer in offers:
                offer.external_id = uuid.uuid4()
                offer.save()
        self.message_user(request, _("UUIDs have been successfully generated!"), messages.SUCCESS)

    def cancel_listing_using_externalID_admin(self, request, queryset):
        api_property_global.cancel_properties_using_externalID()
        self.message_user(request, _("Properties have been successfully removed!"), messages.SUCCESS)

    def delete_images_property_admin(self, request, queryset):
        for prop in queryset:
            api_property_global.delete_images_property(prop)
        self.message_user(request, _("Images have been successfully removed from Global!"), messages.SUCCESS)

    def get_all_properties_admin(self, request, queryset):
        api_property_global.get_properties()
        self.message_user(request, _("All properties list!"), messages.SUCCESS)

    def modify_listed_properies_admin(self, request, queryset):
        api_property_global.modify_listed_properies()
        self.message_user(request, _("Delete properties that doesn't exist on our database!"), messages.SUCCESS)

    def migrate_external_id_from_image_to_json_admin(self, request, queryset):
        api_property_global.migrate_external_id_from_image_to_json()
        self.message_user(request, _("Migrated external ids from image to json"), messages.SUCCESS)
    def migrate_external_id_from_property_to_offer_admin(self, request, queryset):
        api_property_global.migrate_external_id_from_property_to_offer()
        self.message_user(request, _("Migrated external ids from property to offer"), messages.SUCCESS)

    create_property_admin.short_description = _("Create property to REMAX Global")
    cancel_listing_admin.short_description = _("Remove property from REMAX Global")
    generate_uuid_admin.short_description = _("Generate UUIDs")
    cancel_listing_using_externalID_admin.short_description = _("Remove property from REMAX Global using GET request")
    update_property_admin.short_description = _("Update properties from REMAX Global")
    delete_images_property_admin.short_description = _("Remove all images of a promoted property")
    get_all_properties_admin.short_description = _("Get all properties")
    modify_listed_properies_admin.short_description = _("Delete from global properties that doesn't exist on our database")
    migrate_external_id_from_property_to_offer_admin.short_description = _("Migrate external id from property to offer")
    migrate_external_id_from_image_to_json_admin.short_description = _("Migrate external id from image to json")


class PropertyImageFilter(admin.SimpleListFilter):
    title = "Image filter for global"
    parameter_name = "image_offer"

    def lookups(self, request, model_admin):
        return (
            ('all', _('All images')),
            ('images', _('Images for promoted to global properties'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() == 'images':
            return queryset.filter(~Q(rex_ids={}))

class PropertyImageAdmin(admin.ModelAdmin):
    list_filter = (PropertyImageFilter,)
    actions = ['update_image_property', 'delete_one_image_property']
    search_fields = ('property__id', )

    def delete_one_image_property(self, request, queryset):
        for img in queryset:
            offers = Offer.objects.filter(property=img.property)
            for ofr in offers:
                api_property_global.delete_one_image_property(offer=ofr, image=img)
        self.message_user(request, _("Image was succesfully deleted from promoted property!"), messages.SUCCESS)

    def update_image_property(self, request, queryset):
        id_img = 1
        for image in queryset:
            if image.rex_id:
                offers = Offer.objects.filter(property=image.property)
                for offer in offers:
                    response = api_property_global.update_image_property(image, id_img, offer)
                    if not( 200 <= response < 300):
                        self.message_user(request, _(f"Error while updating image: {image}"))
                        break
                id_img += 1
        self.message_user(request, _("Image was succesfully updated from promoted property!"), messages.SUCCESS)

    delete_one_image_property.short_description = _("Remove image of a promoted property")
    update_image_property.short_description = _("Update image of a promoted property")

admin.site.register(FeatureGroup, FeatureGroupAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(HouseAttributes)
admin.site.register(ApartmentAttributes)
admin.site.register(CommercialAttributes)
admin.site.register(StudioAttributes)
admin.site.register(ComplexAttributes)
admin.site.register(LandAttributes)
admin.site.register(HotelAttributes)
admin.site.register(CabinAttributes)
admin.site.register(GarageAttributes)
admin.site.register(BasementParkingAttributes)
admin.site.register(StorageRoomAttributes)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(PropertyDocument)