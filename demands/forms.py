from django import forms
from django.forms import ModelChoiceField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import ugettext_lazy as _


from crm.utils import get_office, get_user
from demands.models import Demand
from locations.models import City, Zone
from users.models import User
from crm.settings.settings import DATE_INPUT_FORMATS

class DemandForm(forms.ModelForm):
    price_min = forms.IntegerField()

    contract_signing_date = forms.DateField(
    required=False,
    widget=forms.DateInput(attrs={'type':'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy',}),
    label=_('Contract register date'),
    )

    contract_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type':'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy'}),
        label=_('Contract start date'),
    )

    limit_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type':'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy'}),
        label=_('Limit date')
    )

    user = ModelChoiceField(queryset=None, required=False)


    class Meta:
        model = Demand
        exclude = ['created_at', 'updated_at', 'office']

    def __init__(self, *args, **kwargs):
        super(DemandForm, self).__init__(*args, **kwargs)
        # Affects DemandUpdateForm
        self.fields['user'].queryset = User.objects.filter(office=get_office(), is_active=True)
        if self.instance:
            try:
                self.fields['city'].queryset = City.objects.filter(region_id=int(self.instance.region_id)).order_by(
                    'name')
                self.fields['zones'].queryset = Zone.objects.filter(city_id=int(self.instance.city_id)).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['city'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['zones'].queryset = Zone.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset


class DemandUpdateForm(DemandForm):

    country = CountryField().formfield(
        required=False,
        widget=CountrySelectWidget(
           attrs={"class": "my-class"}
        )
    )
    final_price=forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'id': 'final_price_demand'}))
    class Meta:
        model = Demand
        exclude = ['created_at', 'updated_at', 'office']