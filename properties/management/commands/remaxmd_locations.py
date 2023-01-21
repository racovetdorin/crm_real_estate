import json

from django.core.management import BaseCommand
from locations.models import Country, Region, City, Street, Zone


class Command(BaseCommand):
    def handle(self, **options):
        # change files location here
        files_locations = '/app/remaxmd_db/'

        db_offers = f'{files_locations}offers.json'

        counter = 0

        if not Country.objects.filter(name='Republica Moldova').first():
            Country.objects.create(name='Republica Moldova', code='MDA')
            print('Creating country object: Republica Moldova')
            counter += 1

        country = Country.objects.get(name='Republica Moldova')

        if not Region.objects.filter(name='Chisinau').first():
            Region.objects.create(name='Chisinau', country=country)
            print('Creating region object: Chisinau')
            counter += 1

        region = Region.objects.get(name='Chisinau')

        with open(db_offers, 'r') as f_obj:
            db_offers_to_dict_list = json.loads(f_obj.read())

            for obj in db_offers_to_dict_list:
                if obj['city']:
                    if not City.objects.filter(name=obj['city'], region=region).first():
                        City.objects.create(name=obj['city'], region=region)
                        print(f'Creating city object: {obj["city"]}')
                        counter += 1

                    city = City.objects.get(name=obj['city'])

                    if obj['street']:
                        if not Street.objects.filter(name=obj['street'], city=city):
                            Street.objects.create(name=obj['street'], city=city)
                            print(f'Creating street object: {obj["street"]}')
                            counter += 1

        print(f'\nDone! {counter} location objects created.')
