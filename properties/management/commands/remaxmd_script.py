import json

from django.core.management import BaseCommand

from clients.models import Client
from locations.models import Region, City, Street, Zone
from offers.models import Offer
from offices.models import Office
from properties.models import Property, PropertyImage, ApartmentAttributes, HouseAttributes, LandAttributes, \
    CommercialAttributes
from users.models import User
import requests


def upload_images(url, index, property):
    try:
        name = url.split('/')[-1]
        files = {'file': (name, requests.get(url).content, "image/jpeg")}

        #if not PropertyImage.objects.filter(image_name=name).first():
        r = requests.post(f'http://crm.rmx.casa/properties/upload_images/{property.id}/',
                          files=files)
        try:
            property_image = PropertyImage.objects.get(image_name=name)
            property_image.position = index
            property_image.public = True
            property_image.hide_on_site = False
            property_image.deleted = False
            property_image.save()
        except Exception as e:
            print(str(e))
    except Exception as e:
        print(str(e))


class Command(BaseCommand):
    def handle(self, **options):
        # change files location here
        files_locations = '/app/remaxmd_db/'

        db_agencies = f'{files_locations}agencies.json'
        db_agents = f'{files_locations}agents.json'
        db_offers = f'{files_locations}offers.json'
        db_ensembles = f'{files_locations}ensembles.json'

        with open(db_agencies, 'r') as f_obj:
            db_agencies_to_dict_list = json.loads(f_obj.read())
            counter = 1

            for obj in db_agencies_to_dict_list:
                if Office.objects.filter(id=obj['id']).first():
                    print(f'Office: {counter}/{len(db_agencies_to_dict_list)}')
                    continue

                Office.objects.create(id=obj['id'], name=obj['full_name'], email=obj['email'], phone_1=obj['phone'],
                                      address=obj['address'])

                print(f'Office: {counter}/{len(db_agencies)}')
                counter += 1

        with open(db_agents, 'r') as f_obj:
            db_agents_to_dict_list = json.loads(f_obj.read())
            counter = 1

            for obj in db_agents_to_dict_list:
                if User.objects.filter(id=obj['id']).first():
                    print(f'User: {counter}/{len(db_agents_to_dict_list)}')
                    continue

                User.objects.create(id=obj['id'], first_name=obj['first_name'], last_name=obj['last_name'],
                                    email=obj['email'], phone=obj['phone'], office=Office.objects.get(id=135))

                print(f'User: {counter}/{len(db_agencies)}')
                counter += 1

        with open(db_offers, 'r') as f_obj:
            db_offers_to_dict_list = json.loads(f_obj.read())
            counter = 0

            types = {
                'apartment_type': Property.Type.APARTMENT,
                'commercial_building_type': Property.Type.COMMERCIAL,
                'house_type': Property.Type.HOUSE,
                'land_type': Property.Type.LAND
            }

            attributes_object = {
                'apartment_type': ApartmentAttributes,
                'house_type': HouseAttributes,
                'commercial_building_type': CommercialAttributes,
                'land_type': LandAttributes
            }

            for obj in db_offers_to_dict_list:

                for type in types:
                    if obj.get(type):
                        property_type = types[type]
                        AttributesObject = attributes_object[type]
                        break

                counter += 1
                property = Property.objects.filter(id=obj['id']).first()
                if property:
                    print(f'Property: {counter}/{len(db_offers_to_dict_list)}')

                    if obj.get('full_images'):
                        for idx, url in enumerate(obj['full_images']):
                            upload_images(url, idx, property)

                    continue


                region = Region.objects.filter(name=obj['region']).first() or None
                city = City.objects.filter(name=obj['city']).first() or None
                street = Street.objects.filter(name=obj['street']).first() or None

                print(obj['agent'])

                property = Property.objects.create(id=obj['id'], type=property_type, user=User.objects.get(id=obj['agent']['id']),
                                        office=Office.objects.get(id=135), client=Client.objects.all().first(),
                                        region=region, city=city, street=street, latitude=obj['lat'],
                                        longitude=obj['lng'])

                if property_type == Property.Type.LAND:
                    attributes_object = AttributesObject.objects.create(id=obj['id'], title=obj['title'], description=obj['description'],
                                                    surface_total=obj['surface_total'], surface_util=1,
                                                    surface_built=obj['surface_built'],
                                                    surface_field=obj['surface_land'])

                else:
                    attributes_object = AttributesObject.objects.create(id=obj['id'], title=obj['title'], description=obj['description'],
                                                    surface_total=obj['surface_total'], surface_util=1,
                                                    surface_built=obj['surface_built'],
                                                    surface_field=obj['surface_land'],
                                                    construction_year=obj['building_construction_year'],
                                                    floors=obj['building_floors'], rooms_number=obj['rooms'],
                                                    bathrooms_number=obj['bathrooms'],
                                                    balconies_number=obj['balconies'],
                                                    kitchens_number=obj['kitchens'])

                property.attributes_object = attributes_object
                property.save()

                # if obj.get('full_images'):
                #     for idx, url in enumerate(obj['full_images']):
                #         upload_images(url, idx, property)

                exclusive = False
                if obj['for_sale']:
                    type = Offer.ContractType.SALE
                    price = obj['price_sale']

                    if obj['exclusive_sale']:
                        exclusive = True
                else:
                    type = Offer.ContractType.RENT
                    price = obj['price_rent']

                    if obj['exclusive_rent']:
                        exclusive = True

                Offer.objects.create(id=obj['id'], user=property.user, office=property.office, status=settings.STATUS.ACTIVE, type=type,
                                     property=property, price=price, exclusive=exclusive, promote_site=True)

                print(f'Property: {counter}/{len(db_offers_to_dict_list)}')
