import uuid

from django.contrib import admin
from django.contrib import messages

from users.models import User, UserImage, UserProfile
from eav.forms import BaseDynamicEntityForm
from eav.admin import BaseEntityAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ngettext

from integrations.publisher_remax_global import REXAgentsHandlerAPI

global_api_agents = REXAgentsHandlerAPI()


class UserProfileAdminForm(BaseDynamicEntityForm):
    model = UserProfile


class UserProfileAdmin(BaseEntityAdmin):
    form = UserProfileAdminForm


class UserLayout(BaseEntityAdmin):

    list_display = (
        'id',
        'first_name',
        'last_name',
        'phone',
        'email',
        'office',
        'thumbnail',
        'role',
        'international_id',
        'promote_rex'
    )

    list_filter = (
        'office',
        'role',
        'promote_rex'
    )

    search_fields = 'first_name', 'last_name'

    actions = ['create_agents', 'get_agents', 'update_agents', 'delete_agents', 'delete_all_existing_agents',
               'generate_uuid', 'get_all_agents']

    def create_agents(self, request, queryset):
        qs = queryset.filter(promote_rex=True)
        for agent in qs:
            global_api_agents.create_agent(agent)
        self.message_user(request, _("Agents have been successfully created!"), messages.SUCCESS)

    def update_agents(self, request, queryset):
        qs = queryset.filter(promote_rex=True)
        for agent in qs:
            global_api_agents.update_agent(agent)
        self.message_user(request, _("Agents have been successfully updated!"), messages.SUCCESS)

    def delete_agents(self, request, queryset):
        qs = queryset.filter(promote_rex=True)
        for agent in qs:
            global_api_agents.cancel_agent(agent)
        self.message_user(request, _("Agents have been successfully removed!"), messages.SUCCESS)

    def delete_all_existing_agents(self, request, queryset):
        global_api_agents.cancel_agents_using_externalID()
        self.message_user(request, _("All agents from REMAX GLOBAL have been removed"), messages.SUCCESS)

    def generate_uuid(self, request, queryset):
        for user in queryset:
            user.external_id = uuid.uuid4()
            user.save()
        self.message_user(request, _("UUIDs have been successfully generated!"), messages.SUCCESS)
    
    def get_all_agents(self, request, queryset):
        global_api_agents.get_agents()
        self.message_user(request, _("Get all agents"), messages.SUCCESS)


    create_agents.short_description = _("Create agents for global")
    update_agents.short_description = _("Update agents listed to global")
    delete_agents.short_description = _("Remove agents from global")
    delete_all_existing_agents.short_description = _("Remove agents from global using json request")
    generate_uuid.short_description = _("Generate UUIDs")



admin.site.register(User, UserLayout)
admin.site.register(UserImage)
admin.site.register(UserProfile, UserProfileAdmin)
