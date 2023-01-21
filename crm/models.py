from django.conf import settings
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models


class SoftDeleteQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_at = timezone.now()
            obj.deleted = True
            obj.save()


class SoftDeleteManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted=False)


class SoftDeleteModel(models.Model):
    class Meta:
        abstract = True

    deleted = models.BooleanField(db_index=True, default=False, verbose_name=_('Deleted'))
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Deleted At'))

    objects = SoftDeleteManager()
    original_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()


class ImageModel(SoftDeleteModel):
    class Meta:
        abstract = True
        ordering = ['position']

    hide_on_site = models.BooleanField(default=False, verbose_name=_('Hide on site'))
    image_path = models.CharField(max_length=255, verbose_name=_('Image path'))
    image_name = models.CharField(max_length=255, verbose_name=_('Image name'), blank=True, null=True)
    position = models.PositiveIntegerField(verbose_name=_('Image Position'), default=100)


class DocumentModel(SoftDeleteModel):
    class Meta:
        abstract = True

    document_path = models.CharField(max_length=255, verbose_name=_('Image path'))
    document_name = models.CharField(max_length=255, verbose_name=_('Image name'), blank=True, null=True)
