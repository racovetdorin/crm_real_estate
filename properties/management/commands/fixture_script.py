# manage.py script that iterates over all Property objects and replaces the attributes_type_id with the current DB's
# content_type objects ids. The script is used for overwriting inaccurate property.attributes_type_id inherited from
# the DB the fixtures were created from.

from properties.models import Property
from django.contrib.auth.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        for property in Property.objects.all():
            if hasattr(property, 'type'):
                property.attributes_type_id = ContentType.objects.get(model=property.type + 'attributes').id
                property.save()
