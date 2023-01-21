from django.contrib import admin, messages

from demands.models import Demand, LeadSource

class DemandAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'type',
        'property_type',
        'final_price',
        'commission',
        'commission_percent',
        'commission_buyer',
        'commission_buyer_percent',
        'is_closed',
        'closing_date',
        )
    actions = ['remove_demands']

    def remove_demands(self, request, queryset):
        for q in queryset:
            q.delete()
        self.message_user(request, "Delete selected demands.", messages.SUCCESS)
    remove_demands.short_description="Delete selected demands"


admin.site.register(Demand, DemandAdmin)
admin.site.register(LeadSource)
