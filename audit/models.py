import json
from copy import deepcopy
from datetime import datetime, date

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core import serializers
from django.db import models
from django.db.models.fields.files import FieldFile
from django.forms import model_to_dict
from django.utils.itercompat import is_iterable
from django.utils.translation import ugettext_lazy as _

from crm.models import SoftDeleteModel
from crm.utils import get_user
from users.models import User


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = deepcopy(self._dict)

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = deepcopy(self._dict)

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


class AuditableModel(ModelDiffMixin, models.Model):
    IGNORE_FIELDS = []
    DATA_FORMAT = 'json'

    audits = GenericRelation('audit.AuditLog')

    class Meta:
        abstract = True

    def create_audit(self, **kwargs):
        field_changes = self.diff

        if "child" in kwargs.keys():
            field_changes = kwargs.pop('child').diff

        field_changes = self.update_field_changes_data(field_changes)
        audit = AuditLog(object=self, field_changes=field_changes, **kwargs)
        fields = [field.name for field in self._meta.get_fields() if field.name not in self.IGNORE_FIELDS]
        if 'country' in fields:
            return
        audit.data = json.loads(serializers.serialize(self.DATA_FORMAT, [self], fields=fields))[0]

        if audit.action_type in [AuditLog.Type.UPDATED,
                                 AuditLog.Type.ATTRIBUTES_UPDATED,
                                 AuditLog.Type.OFFER_UPDATED] and not field_changes:
            return

        audit.user = get_user()
        audit.save()

    def update_field_changes_data(self, field_changes_data):
        """
        Update a field_name: (old value, new value) style comment data
        dictionary before saving the data and rendering a comment.

        By default, return the dict unchanged.
        """
        for k, v in field_changes_data.items():
            if isinstance(v, (datetime, date)):
                field_changes_data[k] = str(v)
            elif is_iterable(v) and any(isinstance(x, (datetime, date)) for x in v):
                field_changes_data[k] = (str(v[0]), str(v[1]))

        return field_changes_data


class AuditLog(models.Model):
    class Type(models.TextChoices):
        CREATED = 'created', _('Created')
        UPDATED = 'updated', _('Updated')
        DELETED = 'deleted', _('Delete')
        AGENT_CHANGED = 'agent_changed', _('Agent Changed')
        OFFER_CREATED = 'offer_created', _('Offer Created')
        OFFER_UPDATED = 'offer_updated', _('Offer Updated')
        ATTRIBUTES_UPDATED = 'attributes_updated', _('Attributes Updated')
        OTHER = 'other', _('Others')

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=_('Agent'))

    action_type = models.CharField(max_length=256, choices=Type.choices, default=Type.OTHER,
                                   verbose_name=_('Action type'))

    field_changes = models.JSONField(blank=True, null=True, verbose_name=_('Field Changes'))
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Description'))

    object_type = models.ForeignKey('contenttypes.ContentType', related_name='audit_logs', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    object = GenericForeignKey('object_type', 'object_id')

    child_object_type = models.ForeignKey('contenttypes.ContentType', blank=True, null=True, on_delete=models.CASCADE)
    child_object_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    child_object = GenericForeignKey('child_object_type', 'child_object_id')

    data = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.description:
            self._compile_description()

        super().save(*args, **kwargs)

    def get_created_description(self):
        return f"{self.object_type} - #{self.object_id} created"

    def get_updated_description(self):
        return f"{self.object_type} - #{self.object_id} update"

    def get_deleted_description(self):
        return f"{self.object_type} - #{self.object_id} deleted"

    def get_agent_updated_description(self):
        return f"Agent updated on {self.object_type} - #{self.object_id}"

    def get_offer_created_description(self):
        return f"Offer(#{self.child_object_id}) created for {self.object_type} - #{self.object_id}"

    def get_offer_updated_description(self):
        return f"Offer(#{self.child_object_id}) updated on Property - #{self.object_id}"

    def get_attributes_updated_description(self):
        return f"Attributes(#{self.child_object_id}) updated on Property - #{self.object_id}"

    def _compile_description(self):
        get_details_function = 'get_%s_description' % self.action_type

        if hasattr(self, get_details_function):
            self.description = getattr(self, get_details_function)()
