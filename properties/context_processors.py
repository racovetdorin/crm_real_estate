import datetime
from django.conf import settings
from offers.models import Notification, Offer


def custom_context(request):
    offers_notifications = None
    if not request.user.__class__.__name__ == 'AnonymousUser':
        today = datetime.datetime.now()
        expiry_date = today + datetime.timedelta(5)
        expiring_offers = Offer.objects.filter(user=request.user,
                                               contract_end_date__range=(
                                                   today, expiry_date))
        for expiring_offer in expiring_offers:
            if not Notification.objects.filter(offer_id=expiring_offer.id).first():
                title = f'Offer #{expiring_offer.id} expires on {expiring_offer.contract_end_date}'
                Notification.objects.create(title=title, offer=expiring_offer)

        offers_notifications = Notification.objects.filter(offer_id__in=expiring_offers.values_list('id', flat=True),
                                                           offer__is_closed=False,
                                                           offer__status__in=['incomplete', 'active', 'reserved', ])
        notifications_length = len(offers_notifications)

        return {
            'DATE_FORMAT_RO': settings.DATE_FORMAT_RO,
            'DATETIME_FORMAT_RO': settings.DATETIME_FORMAT_RO,
            'LOGO': settings.LOGO,
            'FAVICON': settings.FAVICON,
            'TRADEMARK': settings.TRADEMARK,
            'TITLE': settings.TITLE,
            'CDN_MEDIA_URL': settings.CDN_MEDIA_URL,
            'OFFERS_NOTIFICATIONS': offers_notifications,
            'NOTIFICATIONS_LENGTH': notifications_length,
        }
    else:
        return {
            'DATE_FORMAT_RO': settings.DATE_FORMAT_RO,
            'DATETIME_FORMAT_RO': settings.DATETIME_FORMAT_RO,
            'LOGO': settings.LOGO,
            'FAVICON': settings.FAVICON,
            'TRADEMARK': settings.TRADEMARK,
            'TITLE': settings.TITLE,
            'CDN_MEDIA_URL': settings.CDN_MEDIA_URL,
        }
