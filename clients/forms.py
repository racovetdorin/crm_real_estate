import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from clients.models import Client
from users.models import User


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = [
            'first_name', 'last_name', 'email', 'phone_1', 'phone_2', 'phone_3', 'prefix_1', 'prefix_2', 'prefix_3',
            'company', 'is_agency', 'is_private', 'address', 'national_id', 'is_owner', 'is_buyer', 'is_visible'
        ]

    def clean(self):
        cleaned_data = super().clean()
        phones_keys = ['phone_1', 'phone_2', 'phone_3']
        phones = []

        for phone_key in phones_keys:
            if cleaned_data[phone_key]:
                phones.append(re.sub('[^0-9]', '', str(self.cleaned_data[phone_key])))


        for phone_nr in phones:
            if re.match('(?<!\d)[1-9]\d*(?!\d)', phone_nr) is None:
                self.add_error(None, _("Phone numbers cannot start with 0 !"))


        if len(phones) != len(set(phones)):
            self.add_error(None, _('Phone numbers must be different from one another'))

        for idx, phone in enumerate(phones):
            if len(phone) > 11:
                self.add_error(_(phones_keys[idx]), _('Phone number can have a maximum of 11 characters'))

        return cleaned_data


class ClientUpdateForm(forms.ModelForm):
    agents = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label=_("Change agent"))
    class Meta:
        model = Client
        fields = [
            'first_name', 'last_name', 'email', 'phone_1', 'phone_2', 'phone_3', 'prefix_1', 'prefix_2', 'prefix_3',
            'company', 'is_agency', 'is_private', 'address', 'national_id', 'is_owner', 'is_buyer', 'is_visible'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        self.fields['agents'].queryset = User.objects.filter(office=self.request.user.office)
        

    def clean(self):
        cleaned_data = super().clean()
        phones_keys = ['phone_1', 'phone_2', 'phone_3']
        phones = []

        for phone_key in phones_keys:
            if cleaned_data[phone_key]:
                phones.append(re.sub('[^0-9]', '', str(self.cleaned_data[phone_key])))


        for phone_nr in phones:
            if re.match('(?<!\d)[1-9]\d*(?!\d)', phone_nr) is None:
                self.add_error(None, _("Phone numbers cannot start with 0 !"))


        if len(phones) != len(set(phones)):
            self.add_error(None, _('Phone numbers must be different from one another'))

        for idx, phone in enumerate(phones):
            if len(phone) > 11:
                self.add_error(_(phones_keys[idx]), _('Phone number can have a maximum of 11 characters'))


        return cleaned_data



