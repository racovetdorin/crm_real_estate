import uuid


from offers.models import Offer
from properties.models import Property
from integrations.publisher_remax_global import REXPropertiesHandlerAPI
from integrations.publisher_999 import PropertiesHandler999API

def create_advert_999_task(property):
    offers = Offer.objects.filter(property=property)
    api_properties_999 = PropertiesHandler999API()
    for offer in offers:
        if (offer.mls_999 is True and offer.mls_999_data == {}):
            if api_properties_999.is_valid_offer_999(offer) is True and offer.is_closed is False:
                api_properties_999.create_advert_999(offer)
        elif (offer.mls_999 is True and offer.advert_id_999 != ''):
            if api_properties_999.is_valid_offer_999(offer) is True and offer.is_closed is False:
                api_properties_999.update_advert_999(offer)
                

def delete_rex_offer(property_id):
    property = Property.objects.get(id=property_id)
    api_properties_global = REXPropertiesHandlerAPI()
    offers = Offer.objects.filter(property=property)
    for offer in offers:
        api_properties_global.cancel_listing(offer, property)


def update_rex_offer(property_id):
    property = Property.objects.get(id=property_id)
    api_properties_global = REXPropertiesHandlerAPI()
    offers = Offer.objects.filter(property=property)
    for offer in offers:
        if offer:
            if (
                offer.mls_remax_global is True and
                offer.mls_remax_global_data == {} and
                offer.promote_site is True
            ):
                if api_properties_global.is_valid_offer(offer) is True and offer.is_closed is False:
                    response = api_properties_global.create_property(property, offer)
                    if response[0] is None and response[1] is None and response[2] is None and response[3] is None:
                        return
                    if not (200 <= response[0].status_code < 300):
                        offer.mls_remax_global_data['is_created'] = False
                        offer.save()
                        return
                    # Property response json
                    if not (200 <= response[1].status_code < 300):
                        offer.mls_remax_global_data['is_created'] = False
                        offer.save()
                        return
                    # Property eng description update response json
                    if response[2] is not None:
                        if not (200 <= response[2].status_code < 300):
                            offer.mls_remax_global_data['is_created'] = False
                            offer.save()
                            return
                    offer.mls_remax_global_data = response[0].json()
                    offer.mls_remax_global_data['is_created'] = True
                    offer.save()

            elif (
                offer.mls_remax_global is True and
                offer.mls_remax_global_data.get('is_created') is True and
                offer.promote_site is True
            ):
                if api_properties_global.is_valid_offer(offer) is True and offer.is_closed is False:
                    response = api_properties_global.update_property(property, offer)
                    if response[0] is None and response[1] is None and response[2] is None and response[3] is None:
                        return
                    if not (200 <= response[0].status_code < 300):
                        return
                    # Property response json
                    if not (200 <= response[1].status_code < 300):
                        return
                    # Property eng description update response json
                    if response[2] is not None:
                        if not (200 <= response[2].status_code < 300):
                            return
                    offer.mls_remax_global_data = response[0].json()
                    offer.mls_remax_global_data['is_created'] = True
                    if offer.status in ['transacted', 'transacted_by_others',
                            'transacted_by_owner'] and offer.closing_date is not None:
                        offer.mls_remax_global_data['is_transacted'] = True
                    offer.save()

            elif (
                    (offer.mls_remax_global is False or
                    (offer.mls_remax_global_data != {} and offer.promote_site is False)) and
                    offer.mls_remax_global_data.get('is_created') is True
            ):
                response = api_properties_global.cancel_listing(offer, property)
                if not (200 <= response.status_code < 300):
                    return
                else:
                    offer.mls_remax_global_data = {}
                    offer.mls_remax_global = False
                    offer.external_id = uuid.uuid4()
                    offer.save()
            elif (
                offer.mls_remax_global is True and offer.mls_remax_global_data != {} and offer.status in ['incomplete', 'withdrawn', 'pending']
            ):
                if not (200 <= response.status_code < 300):
                    return
                else:
                    offer.mls_remax_global_data = {}
                    offer.mls_remax_global = False
                    offer.external_id = uuid.uuid4()
                    offer.save()

