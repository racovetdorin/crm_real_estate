import datetime
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.forms import modelformset_factory

from offers.models import Offer


class OfferForm(forms.ModelForm):
    type = forms.HiddenInput()

    contract_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy',}),
        label=_('Contract start date')
    )

    contract_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy',}),
        label = _('Contract end date')
    )

    contract_register_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy',}),
        label=_('Contract register date')
    )

    class Meta:
        model = Offer
        exclude = ['user', 'office', 'property', 'deleted_at', 'external_id']


OfferFormSet = modelformset_factory(Offer, form=OfferForm, extra=1)
