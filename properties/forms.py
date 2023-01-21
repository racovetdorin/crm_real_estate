from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import TextInput, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from crm.utils import get_office
from properties.models import Property, ApartmentAttributes, HouseAttributes, StudioAttributes, LandAttributes, \
    HotelAttributes, \
    CommercialAttributes, CabinAttributes, GarageAttributes, BasementParkingAttributes, StorageRoomAttributes, ComplexAttributes
from users.models import User


class PropertyForm(forms.ModelForm):
    block_number = forms.CharField(widget=TextInput(attrs={'placeholder': _('For apartments only')}), required=False,
                                   label=_('Block number'))
    block_entrance_number = forms.CharField(widget=TextInput(attrs={'placeholder': _('For apartments only')}),
                                            required=False, label=_('Block entrance'))
    apartment_number = forms.CharField(widget=TextInput(attrs={'placeholder': _('For apartments only')}),
                                       required=False, label=_('Apartment number'))
    contract_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Property
        fields = [
            'type', 'client', 'region', 'city', 'zone', 'street', 'street_number', 'block_number',
            'block_entrance_number', 'floor', 'apartment_number',
            'virtual_tour', 'video_tour', 'latitude', 'longitude', 'complex'
        ]

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _('A property already exists at this address!'),
            }
        }
    
    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['complex'].queryset = Property.objects.filter(type='complex')
        
        error_border = ['region', 'city', 'city', 'zone', 'floor']
        for field in error_border:
            self.fields[field].required = True

        


class PropertyUpdateForm(forms.ModelForm):
    block_number = forms.CharField(widget=TextInput(attrs={'placeholder': _('For apartments only')}), required=False,
                                   label=_('Block number'))
    
    block_entrance_number = forms.CharField(widget=TextInput(attrs={'placeholder': _('For apartments only')}),
                                            required=False, label=_('Block entrance'))
    apartment_number = forms.CharField(widget=TextInput(attrs={'placeholder': _('For apartments only')}),
                                       required=False, label=_('Apartment number'))
    contract_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    documents = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label=_('Documents'),
                                required=False)

    user = ModelChoiceField(queryset=None, required=False)

    report_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy',}),
        label = _('Report start date')
    )
    
    report_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','data-date-format':'DD/MM/YYYY','data-date':'dd/mm/yyyy',}),
        label = _('Report end date')
    )
    
    floor = forms.CharField(
        required=False,
        label = _('Floor')
    )

    class Meta:
        model = Property
        fields = ['user', 'features', 'client', 'region', 'city', 'zone', 'street', 'street_number', 'block_number',
                  'block_entrance_number', 'floor', 'virtual_tour', 'video_tour',
                  'apartment_number', 'latitude', 'longitude', 'demands_of_interest', 'recommendation', 'conclusion', 'complex', 'report_start_date',
                  'report_end_date' ]

    def __init__(self, *args, **kwargs):
        super(PropertyUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(office=get_office(), is_active=True)
        self.fields['complex'].queryset = Property.objects.filter(type='complex')
        
        error_border = ['region', 'city', 'city', 'zone', 'floor']
        for field in error_border:
            self.fields[field].required = True


class PropertySoftDeleteForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['deleted']


class HouseAttributesForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(HouseAttributesForm, self).__init__(*args, **kwargs)
        error_border = ['description_sentimental', 'subtype', 'description', 
                        'surface_total', 'floors' , 'house_state', 'bathrooms_number', 
                        'water_pipes', 'sewerage', 'gasification', 'description']
        
        for field in error_border:
            self.fields[field].required = True
    
    class Meta:
        model = HouseAttributes
        fields = '__all__'


class ApartmentAttributesForm(forms.ModelForm):
    
    # floor = forms.CharField(label = _('Block entrance'))

    def __init__(self, *args, **kwargs):
        super(ApartmentAttributesForm, self).__init__(*args, **kwargs)
        
        error_border = ['rental_fund', 'surface_total', 'floors', 'rooms_number', 'description']
        for field in error_border:
            self.fields[field].required = True
        
    class Meta:
        model = ApartmentAttributes
        fields = '__all__'

class StudioAttributesForm(forms.ModelForm):
    class Meta:
        model = StudioAttributes
        fields = '__all__'


class CommercialAttributesForm(forms.ModelForm):
    class Meta:
        model = CommercialAttributes
        fields = '__all__'


class LandAttributesForm(forms.ModelForm):
    class Meta:
        model = LandAttributes
        fields = '__all__'


class HotelAttributesForm(forms.ModelForm):
    class Meta:
        model = HotelAttributes
        fields = '__all__'


class CabinAttributesForm(forms.ModelForm):
    class Meta:
        model = CabinAttributes
        fields = '__all__'

class ComplexAttributesForm(forms.ModelForm):
    class Meta:
        model = ComplexAttributes
        fields = '__all__'
class StorageRoomAttributesForm(forms.ModelForm):
    class Meta:
        model = StorageRoomAttributes
        fields = '__all__'

class GarageAttributesForm(forms.ModelForm):
    class Meta:
        model = GarageAttributes
        fields = '__all__'

class BasementParkingAttributesForm(forms.ModelForm):
    class Meta:
        model = BasementParkingAttributes
        fields = '__all__'

