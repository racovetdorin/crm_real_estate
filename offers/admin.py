from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from rangefilter.filters import DateRangeFilter
from django.contrib import messages

from offers.models import Offer, Notification
from integrations.publisher_remax_global import REXPropertiesHandlerAPI
from properties.models import Property


api_property_global = REXPropertiesHandlerAPI()

class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'office',
        'status',
        'type',
        'price',
        'exclusive',
        'final_price',
        'commission',
        'commission_percent',
        'commission_buyer',
        'commission_buyer_percent',
        'commission_success',
        'commission_colaboration',
        'is_closed',
        'closing_date',
        'closed_by',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'user',
        'mls_remax_global',
        'promote_site',
        'office',
        'status',
        'type',
        'is_closed',
        ('closing_date', DateRangeFilter),
        'closed_by',
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter)
    )

    actions = [
        'create_property_admin_offer', 'update_property_admin_offer', 'cancel_listing_admin_offer'
        ]

    def create_property_admin_offer(self, request, queryset):
        """
        Action that promotes a queryset of properties to global
        """
        for offer in queryset:
            prop = Property.objects.filter(offers=offer).first()
            response = api_property_global.create_property(prop, offer)
            if response[0] is None and response[1] is None and response[2] is None and response[3] is None:
                self.message_user(request, _(f"Invalid offer for property: {prop}"))
                break
            if not (200 <= response[0].status_code < 300):
                self.message_user(request, _(f"Error while creating property: {prop}"))
                break
            if not (200 <= response[1].status_code < 300):
                self.message_user(request, _(f"Error while creating description of {prop}"))
                break
            if response[3] is not None:
                self.message_user(request, _(f"Error while creating images of {prop}"))
                break
            if response[2] is not None:
                if not (200 <= response[2].status_code < 300):
                    self.message_user(request, _(f"Error while creating description in ENG of {prop}"))
                    break

        self.message_user(request, _("Properties have been successfully created!"), messages.SUCCESS)

    def update_property_admin_offer(self, request, queryset):
        for offer in queryset:
            prop = Property.objects.filter(offers=offer).first()
            response = api_property_global.update_property(prop, offer)
            if response[0] is None and response[1] is None and response[2] is None and response[3] is None:
                self.message_user(request, _(f"Invalid offer for property: {prop}"))
                break
            if not (200 <= response[0].status_code < 300):
                self.message_user(request, _(f"Error while updating property: {prop}"))
                break
            if not (200 <= response[1].status_code < 300):
                self.message_user(request, _(f"Error while updating description of {prop}"))
                break
            if response[3] is not None:
                self.message_user(request, _(f"Error while updating images of {prop}"))
                break
            if response[2] is not None:
                if not (200 <= response[2].status_code < 300):
                    self.message_user(request, _(f"Error while updating description in ENG of {prop}"))
                    break
        self.message_user(request, _("Properties have been successfully updated!"), messages.SUCCESS)

    def cancel_listing_admin_offer(self, request, queryset):
        for offer in queryset:
            prop = Property.objects.filter(offer=offer)
            response = api_property_global.cancel_listing(offer, prop)
            if not (200 <= response.status_code < 300):
                self.message_user(request, _(f"Error while deleting property: {prop}"))
                break
        self.message_user(request, _("Properties have been successfully removed from Global!"), messages.SUCCESS)

    create_property_admin_offer.short_description = _("Create property to REMAX Global")
    cancel_listing_admin_offer.short_description = _("Remove property from REMAX Global")
    update_property_admin_offer.short_description = _("Update property from REMAX Global")




admin.site.register(Offer, OfferAdmin)
admin.site.register(Notification)
