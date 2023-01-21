from django import forms
from django.utils.translation import ugettext_lazy as _

from users.models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Re-type password'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'groups', 'role', 'office', 'show_on_site', 'is_active', 'display_title']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'groups', 'role', 'office', 'layout_settings', 'show_on_site', 'is_active', 'display_title']
