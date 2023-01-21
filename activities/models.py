from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField

from audit.models import AuditableModel
from clients.models import Client
from crm.models import SoftDeleteModel
from demands.models import Demand
from properties.models import Property
from users.models import User


class Activity(AuditableModel, SoftDeleteModel):
    class Priorities(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')

    class Status(models.TextChoices):
        TO_DO = 'to_do', _('To do')
        IN_PROGRESS = 'in_progress', _('In progress')
        DONE = 'done', _('Done')
        SALE = 'sale', _('Sale leads')
        RENT = 'rent', _('Rent leads')
        PROCESSED = 'processed', _('Processed')

    class Type(models.TextChoices):
        VIEWING = 'viewing', _('Viewing')
        VIRTUAL_VIEWING = 'virtual_viewing', _('Virtual viewing')
        DEMAND_LEAD_GENERATION = 'demand_lead_generation', _('Demand lead generation')
        PROPERTY_LEAD_GENERATION = 'property_lead_generation', _('Property lead generation')
        CLIENT_LEAD_GENERATION = 'client_lead_generation', _('Client lead generation')
        TELEPHONE_CONVERSATION = 'telephone_conversation', _('Telephone conversation')
        PHOTO_VIEWING = 'photo_viewing', _('Photo viewing')

    class Link(models.TextChoices):
        PROPERTY = 'property', _('Property')
        DEMAND = 'demand', _('Demand')
        CLIENT = 'client', _('Client')

    user = models.ForeignKey(User, db_index=True, null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name=_('Agent'))

    type = models.CharField(max_length=256, choices=Type.choices, default='', blank=True,
                            verbose_name=_('Type'))

    linked_with = MultiSelectField(max_length=56, null=True, blank=True, choices=Link.choices,
                                   verbose_name=_('Linked with'))
    property = models.ForeignKey(Property, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Property'))
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Client'))
    demand = models.ForeignKey(Demand, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Demand'))

    title = models.CharField(max_length=100, blank=True, default=_('No title'), verbose_name=_('Title'))
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_('Description'))
    due_date = models.DateField(null=True, blank=True, verbose_name=_('Due date'))
    hyperlink = models.CharField(max_length=256, blank=True, default="", verbose_name=_('Link'))
    phone = models.CharField(max_length=20, blank=True, default="", verbose_name=_('Phone'))

    status = models.CharField(db_index=True, max_length=256, choices=Status.choices, default='', null=True,
                              verbose_name=_('Status'))
    priority = models.CharField(max_length=20, choices=Priorities.choices, blank=True, null=True,
                                verbose_name=_('Priority'))

    is_available = models.BooleanField(default=True, verbose_name=_('Available'))
    is_taken = models.BooleanField(default=False, verbose_name=_('Taken'))
    is_archived = models.BooleanField(db_index=True, default=False, verbose_name=_('Archive'))

    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.title:
            return '{} {}'.format(self.title, self.id)
        else:
            return ''

    def get_absolute_url(self):
        return reverse(settings.ACTIVITIES_LIST_ROUTE)

    def get_display_object_class(self):
        return self.__class__.__name__

    def get_list_background_color_code(self):
        RED = '#FDCECE'
        WHITE = '#FFFFFF'

        if self.is_taken:
            return RED

        return WHITE
