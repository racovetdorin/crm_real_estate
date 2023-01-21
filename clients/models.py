import re

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from audit.models import AuditableModel
from clients.prefixes import Prefix
from crm.models import SoftDeleteModel
from offices.models import Office
from users.models import User


class Client(AuditableModel, SoftDeleteModel):
    first_name = models.CharField(max_length=200, blank=True, verbose_name=_('First name'), default='')
    last_name = models.CharField(max_length=200, blank=True, verbose_name=_('Last name'), default='')
    phone_1 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone 1'))
    phone_2 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone 2'))
    phone_3 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone 3'))
    prefix_1 = models.CharField(max_length=20, choices=Prefix.choices, null=True, blank=True)
    prefix_2 = models.CharField(max_length=20, choices=Prefix.choices, null=True, blank=True)
    prefix_3 = models.CharField(max_length=20, choices=Prefix.choices, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Company'))
    national_id = models.CharField(max_length=56, null=True, blank=True, verbose_name=_('National ID'))
    is_agency = models.BooleanField(default=False, verbose_name=_('Is agency'))
    is_private = models.BooleanField(default=False, verbose_name=_('VIP'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address'))

    user = models.ForeignKey(User, db_index=True, null=True, on_delete=models.SET_NULL, related_name='clients',
                             verbose_name=_('Agent'))
    office = models.ForeignKey(Office, db_index=True, null=True, on_delete=models.SET_NULL, related_name="clients",
                               verbose_name=_('Office'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    is_buyer = models.BooleanField(default=False, verbose_name=_('Is buyer'))
    is_owner = models.BooleanField(default=False, verbose_name=_('Is owner'))
    is_visible = models.BooleanField(default=False, verbose_name=_('Is visible'))

    def __str__(self):
        return self.get_display_full_name()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()

        self.phone_1 = re.sub('[^0-9]', '', str(self.phone_1))
        self.phone_2 = re.sub('[^0-9]', '', str(self.phone_2))
        self.phone_3 = re.sub('[^0-9]', '', str(self.phone_3))

        super().save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse(settings.CLIENTS_UPDATE_ROUTE, args=[self.id])

    def get_whole_phone_1(self):
        return ' '.join([str(x) for x in [self.prefix_1, self.phone_1] if x])

    def get_whole_phone_2(self):
        return ' '.join([str(x) for x in [self.prefix_2, self.phone_2] if x])

    def get_whole_phone_3(self):
        return ' '.join([str(x) for x in [self.prefix_3, self.phone_3] if x])

    def get_display_full_name(self):
        return ' '.join([str(x) for x in [self.first_name, self.last_name] if x])

    def get_display_full_name_with_number_email(self, can_view_details=False):
        display = ''
        if self.first_name:
            display = self.first_name + ' '
        if self.last_name:
            display += self.last_name

        if display:
            display += ' - '

        if can_view_details:
            display += ' / '.join(self._get_list_of_contact_data())
        else:
            display += str(_('Private details for this user'))

        return display

    def get_display_phones(self):
        phones = [self.get_whole_phone_1(), self.get_whole_phone_2(), self.get_whole_phone_3()]

        return ' '.join(phones).strip('None ')

    def get_display_phones_emails_partial_text(self):
        text = self.get_display_phones_emails_text()

        if len(text) > 21:
            text = text[:18] + '...'

        return text

    def get_display_phones_emails_text(self):
        return ' / '.join(self._get_list_of_contact_data())

    def _get_list_of_contact_data(self) -> list:
        contact = []
        contact.append(self.phone_1) if self.phone_1 else None
        contact.append(self.phone_2) if self.phone_2 else None
        contact.append(self.phone_3) if self.phone_3 else None
        contact.append(self.email) if self.email else None

        return contact

    def get_display_object_class(self):
        return self.__class__.__name__

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('prefix_1', 'phone_1'):
            return f''
        else:
            return super(Client, self).unique_error_message(model_class, unique_check)
