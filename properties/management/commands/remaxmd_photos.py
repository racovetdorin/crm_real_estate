import ast
import requests

from django.core.management import BaseCommand
from properties.models import Property, PropertyImage


def upload_images(url, index, property):
    try:
        name = url.split('/')[-1]
        files = {'file': (name, requests.get(url).content, "image/jpeg")}
        # if not PropertyImage.objects.filter(image_name=name).first():
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
        files_locations = '/app/'
        db_images = f'{files_locations}remaxmd_images.json'
        counter = 0

        with open(db_images, 'r') as f_obj:
            db_images_dict = ast.literal_eval(f_obj.read())

        for property_id, images_urls in images.items():
            counter += 1
            property = Property.objects.filter(id=int(property_id)).first()
            if property:
                for image in property.images.values():
                    property_image = PropertyImage.objects.filter(id=image['id']).first()
                    property_image.delete()
                for index, image_url in enumerate(images_urls):
                    upload_images(image_url, index, property)
            print(f'Uploading images for property with id {property.id} ({counter}/{len(db_images_dict)}')
