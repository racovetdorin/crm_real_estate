from django.contrib import admin
from django.contrib import messages
from integrations.publisher_remax_global import REXOfficesHandlerAPI
from offices.models import Office
from django.utils.translation import ugettext_lazy as _
import uuid

api_office_global = REXOfficesHandlerAPI()

class OfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'international_id']

    actions = ['create_office', 'update_office', 'delete_office', 'delete_office_json_request',
               'generate_uuid']

    def create_office(self, request, queryset):
        qs = queryset.filter(international_id__isnull=False)
        for office in qs:
            api_office_global.create_offices(office)
        self.message_user(request, _("Offices have been successfully added!"), messages.SUCCESS)


    def update_office(self, request, queryset):
        qs = queryset.filter(international_id__isnull=False)
        for office in qs:
            api_office_global.update_office(office)
        self.message_user(request, _("Offices have been successfully updated!"), messages.SUCCESS)

    def delete_office(self, request, queryset):
        qs = queryset.filter(international_id__isnull=False)
        for office in qs:
            api_office_global.cancel_office(office)
        self.message_user(request, _("Offices have been successfully removed!"), messages.SUCCESS)

    def delete_office_json_request(self, request, queryset):
        api_office_global.delete_all_listed_offices()
        self.message_user(request, _("Offices have been successfully removed!"), messages.SUCCESS)

    def generate_uuid(self, request, queryset):
        for office in queryset:
            office.external_id = uuid.uuid4()
            office.save()
        self.message_user(request, _("UUIDs have been successfully generated!"), messages.SUCCESS)


    create_office.short_description = _("Create offices to REMAX Global")
    update_office.short_description = _("Update offices from REMAX Global")
    delete_office.short_description = _("Remove listed offices from REMAX Global")
    delete_office_json_request.short_description = _("Remove listed offices from REMAX Global using json request")
    generate_uuid.short_description = _("Generate UUIDs")







admin.site.register(Office, OfficeAdmin)
