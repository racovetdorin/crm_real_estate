from urllib import response
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import django_rq 


from properties.models import Property
from properties.tasks import create_advert_999_task, update_rex_offer, delete_rex_offer


@receiver(post_save, sender=Property)
def update_offer_on_rex(sender, instance, created, *args, **kwargs):
    django_rq.enqueue(update_rex_offer, instance.id)


@receiver(post_delete, sender=Property)
def delete_offer_on_rex(sender, instance, created, *args, **kwargs):
    django_rq.enqueue(delete_rex_offer, instance.id)

@receiver(post_save, sender=Property)
def create_advert_on_999(sender, instance, created, *args, **kwargs):
    django_rq.enqueue(create_advert_999_task, instance)
