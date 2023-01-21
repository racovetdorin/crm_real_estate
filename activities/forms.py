from django import forms
from django.forms import ModelChoiceField
import re

from activities.models import Activity
from crm.utils import get_office
from users.models import User
from django.utils.translation import ugettext_lazy as _


class ActivityForm(forms.ModelForm):
    user = ModelChoiceField(queryset=None, required=False)

    class Meta:
        model = Activity
        fields = ['type', 'title', 'description', 'due_date', 'status', 'priority', 'user',
                  'hyperlink', 'phone', 'is_available', 'is_taken', 'linked_with',
                  'is_archived', 'property', 'client', 'demand']

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(office=get_office(), is_active=True)

