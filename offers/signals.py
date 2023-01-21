# import uuid

# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from offers.models import Offer


# @receiver(post_save, sender=Offer)
# def update_offer_on_rex(sender, offer, **kwargs):
#     if offer.status == settings.STATUS.ACTIVE and offer.mls_remax_global is True:
#         # "Update/create offer on Rex"
#         offer.mls_remax_global_data["is_promoted"] = True
#         offer.save()
#     elif (
#         offer.mls_remax_global is True
#         and offer.status != settings.STATUS.ACTIVE
#         and offer.mls_remax_global_data["is_promoted"] is True
#     ):
#         # Depromovam
#         offer.mls_remax_global_data["is_promoted"] = False
#         offer.save()
#         offer.property.external_id = uuid.uuid4()
#         offer.property.save()
