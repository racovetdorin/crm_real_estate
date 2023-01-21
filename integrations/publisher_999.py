from codecs import latin_1_decode
import re
import requests
import json
import rollbar

from datetime import datetime

from users.models import User
from properties.models import Property
from offers.models import Offer
from crm.filters import get_details_medium_watermarked_thumbnail_url





class PropertiesHandler999API():

    GET_CATEGORIES, GET_PHONE_NUMBERS, CREATE_ADVERT, UPLOAD_IMAGES = 'get_categories', 'get_phone_numbers', 'create_advert', 'upload_images'
    UPDATE_ADVERT = 'update_advert'
    BASE_999_URL = 'https://partners-api.999.md'
    BASE_IMAGE_URL = 'https://media.rmx.casa/'

    

    SUBCATEGORIES = {
        'house': '1406',
        'apartment': '1404',
        'studio': '1404',
        'commercial':'1405',
        'land': '1407',
        'hotel': '1404',
        'cabin': '1404',
        'complex': '1405',
        'basement_parking': '1408',
        'garage': '1408',
        'storage_room':'1408',
    }

    OFFER_TYPES = {
        'sale': '776',
        'rent': '912'
    }

    APARTMENT_FEATURES = {
        'author': {
            '795': '18894'
        },
        'rental_fund': {
            '852': {
                'new_construction': '19108',
                'secondary': '19109',
            }
        },
        'rooms_number': {
            '241': {
                1: '893',
                2: '894',
                3: '902',
                4: '904',
                5: '20442',
                6: '20442',
                7: '20442',
                8: '20442',
                9: '20442',
                10: '20442',
                11: '20442',
                12: '20442',
                13: '20442',
                14: '20442',
                15: '20442',
                16: '20442',
                17: '20442',
                18: '20442',
                19: '20442',
                20: '20442'
            }
        },
        'floor': {
            '248': {
                'basement': '977',
                'semi_basement': '973',
                'ground_floor': '918',
                'entresol_floor': '918',
                'mansard': '12486',
                '1': '918',
                '2': '935',
                '3': '905',
                '4': '929',
                '5': '909',
                '6': '955',
                '7': '895',
                '8': '921',
                '9': '934',
                '10': '947',
                '11': '970',
                '12': '965',
                '13': '958',
                '14': '913',
                '15': '1016',
                '16': '1019',
                '17': '940',
                '18': '1021',
                '19': '1015',
                '20': '1681'
            }
        },
        'floors': {
            '249': {
                1: '956',
                2: '964',
                3: '906',
                4: '936',
                5: '910',
                6: '919',
                7: '971',
                8: '975',
                9: '896',
                10: '951',
                11: '948',
                12: '954',
                13: '966',
                14: '959',
                15: '979',
                16: '914',
                17: '1018',
                18: '1017',
                19: '982',
                20: '972'
            }
        },
        'apartment_construction_material': {
            '247': {
                'concrete': '927',
                'bca': '980',
                'blocks': '932',
                'combined': '945',
                'limestone': '911',
                'brick': '924',
                'wood': '1654',
                'monolith': '942',
                'panels': '897'
            }
        },
        'building_plan': {
            '246': {
                '102':'930',
                '135':'898',
                '143':'943',
                'gostinca': '946',
                'brejnevka': '961',
                'camin_familial': '907',
                'ceska': '969',
                'hrusciovka': '938',
                'individuala': '915',
                'ms_serie_moldoveneasca': '953',
                'pe_pamant': '957', 
                'rubaska': '944',
                'stalinka': '960',
                'vart': '978'
            }
        },
        'surface_total': '244',
        'surface_util': '239',
        'surface_kitchen': '242',
        'ceiling_height': '237',
        'apartment_state': {
            '253': {
                'in_white': '925',
                'in_grey': '949',
                'euro_reparation': '916',
                'individual_design': '937',
                'without_reparation': '928',
                'ready_for_use': '23788',
                'unfinished_construction': '981',
                'need_reparation': '952',
                'cosmetic_reparation': '931',
                'demolition_house': '976'               
            }
        },
        'balconies_number': {
            '250': {
                None: '917',
                1: '920',
                2: '933',
                3: '899',
                4: '974',
                5: '974',
                6: '974',
                7: '974',
                8: '974',
                9: '974',
                10: '974',
            }
        },
        'bathrooms_number': {
            '252': {
                1: '900',
                2: '950',
                3: '967',
                4: '968',
                5: '968',
                6: '968',
                7: '968',
                8: '968',
                9: '968',
                10: '968',
            }
        },
        'garage': {
            '251': {
                'garage': '939',
                'underground_garage': '926',
                'exterior_parking': '901',
                'subscription_parking': '926'
            }
        },
        'anexa':{
            '176': {
                'Debara': True,
                'Magazie': True
            }
        },
        'furnished': '188',
        'household_technique': {
            '214': {
                'Mașină de spălat vase': True,
                'Mașină de spălat rufe': True,
                'Frigider': True,
                'Aragaz': True,
                'Televizor': True,
                'Jacuzzi': True,
            }
        },
        'heating_source': {
            '154': 'individual_central_heating',
            '229': 'underfloor_heating'
        },
        'windows': {
            '223': 'double_glazing'
        },
        'partitioning':{
            '193': 'detached'
        },
        'check_box_features': {
            '182': 'Aer condiționat',
            '196': 'Parchet',
            '160': 'Blindată',
            '226': 'Telefon',
            '175': 'Interfon',
            '179': 'Conexiune internet',
            '225': 'Televizor',
            '217': 'Sistem de alarmă',
            '162': 'Supraveghere video',
            '186': 'Lift',
            '172': 'Gata de intrare',
            '218': 'Sistem casă inteligentă',
            '173': 'Teren de joacă'
        },
        'description_sentimental': '12',
        'description': '13',
        'price': '2',
        'allow_childrens': {
            '1372': {
                'children_are_accepted': '24346',
                'without_children': '24347'
            }
        },
        'allow_animals': {
            '1382': {
                'animals_are_accepted': '24439',
                'without_animals': '24440'
            }
        }
    }
    COMMON_FEATURES = {
        'country': '5',
        'region': '7',
        'city':'8',
        'zone': '9',
        'street': '10',
        'street_number': '11',
        'map': '3'
    }
    
    HOUSE_FEATURES = {
        'author': {
            '795': '18894'
        },
        'subtype': {
            '1311': {
                'detached': '23321',
                'terraced': '23323',
                'attached': '23323'
            }
        },
        'floors': {
            '249': {
                1: '1641',
                2: '1643',
                3: '1644',
                4: '1652',
                5: '1652',
                6: '1652',
                7: '1652',
                8: '1652',
                9: '1652',
                10: '1652',
                11: '1652',
                12: '1652',
                13: '1652',
                14: '1652',
                15: '1652',
                16: '1652',
                17: '1652',
                18: '1652',
                19: '1652',
                20: '1652'
            }
        },
        'house_state': {
            '254':{
                'individual_design': '1653',
                'without_reparation': '1640',
                'demolition_house': '1656',
                'unfinished_construction': '1645',
                'need_reparation': '1646',
                'in_grey': '1650',
                'in_white': '1648',
                'cosmetic_reparation': '1642',
                'euro_reparation': '1649'
            }
        },
        'sewerage': {
            '1623': {
                'without_sewerage': '27760',
                'there_sewer': '27759',
            }
        },
        'water_pipes': {
            '1622': {
                'without_plumbing': '27758',
                'there_running_water': '27757',
            }
        },
        'gasification': {
            '1624': {
                'gasified': '27761',
                'not_gasified': '27762',
            }
        },
        'rooms_number':'588',
        'house_construction_material': {
            '247': {
                'panels': '897',
                'limestone': '911',
                'brick':'924',
                'blocks': '932',
                'monolith': '942',
                'concrete': '927',
                'combined': '945',
                'bca': '980',
                'wood': '1654',
                'other': '1647'
            }
        },
        'surface_field': '245', 
        'surface_total': '244',
        'surface_util': '239',
        'surface_kitchen': '242',
        'ceiling_height':'237',
        'furnished':'187',
        'balconies_number': {
            '250': {
                None: '917',
                1: '920',
                2: '933',
                3: '899',
                4: '974',
                5: '974',
                6: '974',
                7: '974',
                8: '974',
                9: '974',
                10: '974',
            }
        },
        'bathrooms_number': {
            '252': {
                1: '900',
                2: '950',
                3: '967',
                4: '968',
                5: '968',
                6: '968',
                7: '968',
                8: '968',
                9: '968',
                10: '968',
            }
        },
        'household_technique': {
            '214': {
                'Mașină de spălat vase': True,
                'Mașină de spălat rufe': True,
                'Frigider': True,
                'Aragaz': True,
                'Televizor': True,
                'Jacuzzi': True,
            }
        },
        'garage':'170',
        'heating_source': {
            'individual_central_heating': '154',
            'underfloor_heating': '229'
        },
        'check_box_features': {
            'Gata de intrare':'171',
            'Are subsol' :'200',
            'O parte din casă':'232',
            'Lift cu destinație programată': '186',
            'Saună': '216',
            'Bazin': '158',
            'Terasă': '230',
            'Canalizare': '153',
            'Gaz': '169',
            'Grupuri sanitare amenajate și utilate': '164',
            'Aer condiționat': '183',
            'Șemineu': '180',
            'Parchet': '196',
            'Sistem casă inteligentă': '218',
            'Interfon': '175',
            'Telefon': '227',
            'Conexiune internet': '179',
            'Televizor': '225',
            'Sistem de alarmă': '217', 
            'Supraveghere video': '162',
            'Telecomandă poartă acces auto': '166',
            'Grădină': '215',
            'Încăpere pentru servitori / pază': '203',
            'Generator electric': '235',
            'Sistem de purificare a apei': '220',
            'Teren de joacă': '173',
        },
        'windows': {
            'double_glazing': '223'
        },
        'description_sentimental': '12',
        'description': '13',
        'price': '2',
        'allow_childrens': {
            '1372': {
                'children_are_accepted': '24346',
                'without_children': '24347'
            }
        },
        'allow_animals': {
            '1382': {
                'animals_are_accepted': '24439',
                'without_animals': '24440'
            }
        }
    }

    LAND_FEATURES = {
        'subtype': {
            '258': {
                'agricultural_land': '1040',
                'construction_land': '1039'
            }
        },
        'surface_total': '245',
        'check_box_features': {
            '168': 'Gaz',
            '181': 'Canalizare',
            '236': 'Curent', 
            '165': 'Apă',
            '219': 'Irigații',
            '195': 'Pază',
            '227': 'Telefon',
            '155': 'Asfaltate',
            '209': 'Amplasat în localitate',
            '210': 'Amplasat în afara localității',
            '212': 'Alături de un bazin acvatic',
            '213': 'Alături de pădure'
        },
        'description_sentimental': '12',
        'description': '13',
        'price': '2',
    }

    GARAGE_PARKING_FEATURES = {
        'type': {
            '259': {
            'basement_parking': '1043',
            'garage': '1041'
            }
        },
        'check_box_features': {
            '234': 'Electricitate',
            '161': 'Ventilație / evacuare fum',
            '202': 'Sistem de alarmă antiincendiu',
            '221': 'Sistem de stingere a incendiului',
            '184': 'Pază non-stop',
            '1278': 'Pază de noapte',
            '217': 'Sistem de alarmă',
            '162': 'Supraveghere video',
            '222': 'Canal de examinare',
            '194': 'Loc deschis',
            '189': 'Loc sub acoperiș',
            '228': 'Elemente termice'
        },
        'description_sentimental': '12',
        'description': '13',
        'price': '2', 
    }

    COMMERCIAL_FEATURES = {
        'subtype': {
            '257': {
                'commercial_space': '1030',
                'office_space': '1026',
                'industrial_space': '1027'
            }
        },
        'surface_total': '244',
        'surface_util': '1277',
        'commercial_state': {
            '255': {
                'individual_design': '1034',
                'euro_reparation': '1024',
                'without_reparation': '1037',
                'in_white': '1038',
                'in_grey': '1022',
                'need_reparation': '1036',
                'cosmetic_reparation': '1028'
            }
        },
        'floor': {
            '248': {
                'basement': '977',
                'semi_basement': '973',
                'ground_floor': '918',
                'entresol_floor': '918',
                'mansard': '947',
                '1': '918',
                '2': '935',
                '3': '905',
                '4': '929',
                '5': '909',
                '6': '955',
                '7': '895',
                '8': '921',
                '9': '934',
                '10': '947',
                '11': '947',
                '12': '947',
                '13': '947',
                '14': '947',
                '15': '947',
                '16': '947',
                '17': '947',
                '18': '947',
                '19': '947',
                '20': '947'
            }
        },
        'bathrooms_number': {
            '252': {
                1: '900',
                2: '950',
                3: '967',
                4: '968',
                5: '968',
                6: '968',
                7: '968',
                8: '968',
                9: '968',
                10: '968',
            }
        },
        'furnished': '187',
        'heating_source': {
            'individual_central_heating':'154'
        },
        'windows': {
            'double_glazing': '223'
        },
        'kitchens_number': '185',
        'check_box_features': {
            '167': 'La șosea',
            '235': 'Generator de urgență',
            '169': 'Gaz',
            '199': 'Locuri de parcare',
            '183': 'Aer conditionat',
            '179': 'Conexiune internet',
            '186': 'Lift',
            '225': 'Televizor',
            '205': 'Anticameră',
            '162': 'Supraveghere video',
            '178': 'Sală de conferințe',
            '217': 'Sistem de alarmă',
            '201': 'Are subsol',
            '177': 'Pază',
            '157': 'Restaurant în clădire',
            '208': 'Acces secundar marfă'
        },
        'description_sentimental': '12',
        'description': '13',
        'price': '2', 
    }

    def generate_headers_999(self, dict_headers):
        dict_headers['Content-type'] = 'application/json;' 
        return dict_headers

    def generate_header_images_999(self, dict_headers):
        dict_headers['Content-type'] = 'multipart/form-data' 
        return dict_headers

    def generate_url_999(self, type_url, advert_id=None):
        base_url = self.BASE_999_URL
        if type_url == self.GET_CATEGORIES:
            return base_url + '/categories?lang=ro'
        elif type_url == self.GET_PHONE_NUMBERS:
            return base_url + '/phone_numbers?lang=ro'
        elif type_url == self.CREATE_ADVERT:
            return base_url + '/adverts?lang=ro'
        elif type_url == self.UPLOAD_IMAGES:
            return base_url + '/images'
        elif type_url == self.UPDATE_ADVERT:
            return base_url + f'/adverts/{advert_id}?lang=ro'
    
    def is_valid_offer_999(self, offer):
        if offer is None:
            return False
        elif offer.status in ['incomplete', 'withdrawn', 'pending']:
            return False
        elif not offer.promote_site:
            return False
        elif offer.property.user.office.id == 3 and offer.created_at < datetime(2022, 9, 1, 0, 0, 0):
            return False
        return True

    def send_request_999(self, url, username, files=None, headers=None, password='', json=None, type_request=None):
        response = ''
        if type_request == 'GET':
            response = requests.get(url=url, auth=(username, password), headers=headers)
        elif type_request == 'POST':
            response = requests.post(url=url, auth=(username, password), data=json, headers=headers)
        elif type_request == 'IMAGE_POST':
            response = requests.post(url=url, auth=(username, password), files=files)
        elif type_request == 'PATCH':
            response = requests.patch(url=url, auth=(username, password), data=json, headers=headers)
        
        message = f'STATUS CODE (999.md) - {response.status_code}' + f' RESPONSE - {response.text}'

        if 200 <= response.status_code < 300:
            rollbar.report_message(message=message, level='info')
        elif 300 <= response.status_code < 400:
            rollbar.report_message(message=message, level='warning')
        elif response.status_code >= 400:
            rollbar.report_message(message=message, level='error')
        return response
    
    def generate_common_features(self, tags, offer):
        feature_list = []
        for key, value in tags.items():
            if hasattr(offer.property, key) or hasattr(offer.property.user, key):
                if key == 'region' and offer.property.region:
                    region = {'id': value, 'value': str(offer.property.region.id_999)}
                    feature_list.append(region)
                if key == 'city' and offer.property.city:
                    city = {'id': value, 'value': str(offer.property.city.id_999)}
                    feature_list.append(city)
                if key == 'zone' and offer.property.zone is not None:
                    zone = {'id': value, 'value': str(offer.property.zone.id_999)}
                    feature_list.append(zone)
                if key == 'street' and offer.property.street:
                    street = {'id': value, 'value': offer.property.street.name}
                    feature_list.append(street)
                if key == 'street_number' and offer.property.street_number:
                    street_number = {'id': value, 'value': offer.property.street_number}
                    feature_list.append(street_number)
            elif key == 'country':
                country = {'id': value, 'value': '12869'}
                feature_list.append(country)
            elif key == 'map':
                coordinates = {'id': value, 'value': {
                    "lat": offer.property.latitude,
                    "lon": offer.property.longitude,
                    "bearing": 0,
                    "pitch": 0,
                    "zoom": 0,
                }}
                feature_list.append(coordinates)
            
        url = self.generate_url_999(self.GET_PHONE_NUMBERS)
        hdr = {}
        header = self.generate_headers_999(hdr)
        response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header ,type_request='GET')
        phone_numbers_list = []
        if 200 <= response.status_code < 300: 
            response = response.json()
            user_phone = re.sub(r"[^0-9]", "", offer.user.phone)
            for p in response['phone_numbers']:
                phone_number = p['phone_number']
                if user_phone == phone_number:
                    phone_numbers_list.append(phone_number)
                elif offer.office.id != 5:
                    phone_numbers_list.append(phone_number)
            phone = {'id': '16', 'value': [p for p in phone_numbers_list]}
            feature_list.append(phone)
        return feature_list
               

    def generate_json_data_tags_999(self, dict_json , tags, offer):
        property = Property.objects.get(id=offer.property.id)
        if tags == self.SUBCATEGORIES:
            for key, value in tags.items():
                if property.type == key:
                    dict_json['subcategory_id'] = value
        elif tags == self.OFFER_TYPES:
            for key, value in tags.items():
                if offer.type == key:
                    dict_json['offer_type'] = value

    def generate_features_for_commercial_space(self, tags, commercial_offer):
        feature_list = []
        property_features=commercial_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(commercial_offer.property.attributes_object, key) or hasattr(commercial_offer, key) or hasattr(commercial_offer.property, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == commercial_offer.property.attributes_object.subtype:
                                    subtype = {'id': ke, 'value': v}
                                    feature_list.append(subtype)
                                if k == commercial_offer.property.attributes_object.commercial_state:
                                    commercial_state = {'id': ke, 'value': v}
                                    feature_list.append(commercial_state)
                                if k == commercial_offer.property.floor:
                                    floor = {'id': ke, 'value': v}
                                    feature_list.append(floor)
                                if k == commercial_offer.property.attributes_object.bathrooms_number:
                                    bathrooms_number = {'id': ke, 'value': v}
                                    feature_list.append(bathrooms_number)
                if key == 'furnished' and commercial_offer.property.attributes_object.furnished:
                    furnished = {'id': value, 'value': True}
                    feature_list.append(furnished)
                if key == 'heating_source' and commercial_offer.property.attributes_object.heating_source:
                    for ke, va in value.items():
                        if ke == commercial_offer.property.attributes_object.heating_source:
                            heating_source = {'id': va, 'value': True}
                            feature_list.append(heating_source)
                if key == 'windows' and commercial_offer.property.attributes_object.windows:
                    for ke, va in value.items():
                        if ke == commercial_offer.property.attributes_object.windows:
                            windows = {'id': va, 'value': True}
                            feature_list.append(windows)
                if key == 'kitchens_number' and commercial_offer.property.attributes_object.kitchens_number:
                    kitchen = {'id': value, 'value': True}
                    feature_list.append(kitchen)
                if key == 'surface_total' and commercial_offer.property.attributes_object.surface_total:
                    surface_total = {'id': value, 'value': int(commercial_offer.property.attributes_object.surface_total), 'unit': 'm2'}
                    feature_list.append(surface_total)  
                if key == 'surface_util' and commercial_offer.property.attributes_object.surface_util:
                    surface_util = {'id': value, 'value': int(commercial_offer.property.attributes_object.surface_util), 'unit': 'm2'}
                    feature_list.append(surface_util)
                if key == 'description_sentimental' and commercial_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': commercial_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and commercial_offer.property.attributes_object.description:
                    description = {'id': value, 'value': commercial_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and commercial_offer.price:
                    price = {'id': value, 'value': commercial_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
        return feature_list

    def update_generate_features_for_commercial_space(self, tags, commercial_offer):
        feature_list = []
        property_features=commercial_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(commercial_offer.property.attributes_object, key) or hasattr(commercial_offer, key) or hasattr(commercial_offer.property, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == commercial_offer.property.attributes_object.subtype:
                                    subtype = {'id': ke, 'value': v}
                                    feature_list.append(subtype)
                                if k == commercial_offer.property.attributes_object.commercial_state:
                                    commercial_state = {'id': ke, 'value': v}
                                    feature_list.append(commercial_state)
                                if key == 'floor':
                                    if k == commercial_offer.property.floor:
                                        floor = {'id': ke, 'value': v}
                                        feature_list.append(floor)
                                    elif commercial_offer.property.floor is None:
                                        floor = {'id': ke, 'value': None}
                                        feature_list.append(floor)
                                if key == 'bathrooms_number':
                                    if k == commercial_offer.property.attributes_object.bathrooms_number:
                                        bathrooms_number = {'id': ke, 'value': v}
                                        feature_list.append(bathrooms_number)
                                    elif commercial_offer.property.attributes_object.bathrooms_number is None:
                                        bathrooms_number = {'id': ke, 'value': None}
                                        feature_list.append(bathrooms_number)
                if key == 'furnished':
                    if commercial_offer.property.attributes_object.furnished:
                        furnished = {'id': value, 'value': True}
                        feature_list.append(furnished)
                    elif not commercial_offer.property.attributes_object.furnished:
                        furnished = {'id': value, 'value': None}
                        feature_list.append(furnished)
                if key == 'heating_source':
                    for ke, va in value.items():
                        if ke == commercial_offer.property.attributes_object.heating_source:
                            heating_source = {'id': va, 'value': True}
                            feature_list.append(heating_source)
                        elif ke != commercial_offer.property.attributes_object.heating_source:
                            heating_source = {'id': va, 'value': None}
                            feature_list.append(heating_source)
                if key == 'windows':
                    for ke, va in value.items():
                        if ke == commercial_offer.property.attributes_object.windows:
                            windows = {'id': va, 'value': True}
                            feature_list.append(windows)
                        elif ke == commercial_offer.property.attributes_object.windows:
                            windows = {'id': va, 'value': None}
                            feature_list.append(windows)
                if key == 'kitchens_number': 
                    if commercial_offer.property.attributes_object.kitchens_number:
                        kitchen = {'id': value, 'value': True}
                        feature_list.append(kitchen)
                    elif not commercial_offer.property.attributes_object.kitchens_number:
                        kitchen = {'id': value, 'value': None}
                        feature_list.append(kitchen)
                if key == 'surface_total' and commercial_offer.property.attributes_object.surface_total:
                    surface_total = {'id': value, 'value': int(commercial_offer.property.attributes_object.surface_total), 'unit': 'm2'}
                    feature_list.append(surface_total)  
                if key == 'surface_util' and commercial_offer.property.attributes_object.surface_util:
                    surface_util = {'id': value, 'value': int(commercial_offer.property.attributes_object.surface_util), 'unit': 'm2'}
                    feature_list.append(surface_util)
                if key == 'description_sentimental' and commercial_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': commercial_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and commercial_offer.property.attributes_object.description:
                    description = {'id': value, 'value': commercial_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and commercial_offer.price:
                    price = {'id': value, 'value': commercial_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
                            if feature_list.count({'id': ke, 'value': None}) > 0:
                                feature_list.remove({'id': ke, 'value': None})
                        elif feature.name != va and feature_list.count({'id': ke, 'value': True}) == 0 and feature_list.count({'id': ke, 'value': None}) == 0:
                            ac = {'id': ke, 'value': None}
                            feature_list.append(ac)
        return feature_list

    def generate_features_for_garage_and_parking(self, tags, gp_offer):
        feature_list = []
        property_features=gp_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(gp_offer.property.attributes_object, key) or hasattr(gp_offer, key) or hasattr(gp_offer.property, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == gp_offer.property.type:
                                    type = {'id': ke, 'value': v}
                                    feature_list.append(type)
                if key == 'description_sentimental' and gp_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': gp_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and gp_offer.property.attributes_object.description:
                    description = {'id': value, 'value': gp_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and gp_offer.price:
                    price = {'id': value, 'value': gp_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
        return feature_list
    
    def update_generate_features_for_garage_and_parking(self, tags, gp_offer):
        feature_list = []
        property_features=gp_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(gp_offer.property.attributes_object, key) or hasattr(gp_offer, key) or hasattr(gp_offer.property, key):
                if key == 'type':
                    for ke, va in value.items():
                        for k, v in va.items():
                            if k == gp_offer.property.type:
                                type = {'id': ke, 'value': v}
                                feature_list.append(type)
                if key == 'description_sentimental' and gp_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': gp_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and gp_offer.property.attributes_object.description:
                    description = {'id': value, 'value': gp_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and gp_offer.price:
                    price = {'id': value, 'value': gp_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
                            if feature_list.count({'id': ke, 'value': None}) > 0:
                                feature_list.remove({'id': ke, 'value': None})
                        elif feature.name != va and feature_list.count({'id': ke, 'value': True}) == 0 and feature_list.count({'id': ke, 'value': None}) == 0:
                            ac = {'id': ke, 'value': None}
                            feature_list.append(ac)
        return feature_list

    def generate_features_for_lands(self, tags, land_offer):
        feature_list = []
        property_features=land_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(land_offer.property.attributes_object, key) or hasattr(land_offer, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == land_offer.property.attributes_object.subtype:
                                    subtype = {'id': ke, 'value': v}
                                    feature_list.append(subtype)
                if key == 'surface_total' and land_offer.property.attributes_object.surface_total:
                    if land_offer.property.attributes_object.units_of_measure in ['square_meters', 'acres']:
                        surface_field = {'id': value, 'value': int(land_offer.property.attributes_object.surface_total), 'unit': 'ar' }
                    else:
                        surface_field = {'id': value, 'value': int(land_offer.property.attributes_object.surface_total), 'unit': 'ha' }
                    feature_list.append(surface_field)
                if key == 'description_sentimental' and land_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': land_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and land_offer.property.attributes_object.description:
                    description = {'id': value, 'value': land_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and land_offer.price:
                    price = {'id': value, 'value': land_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
        return feature_list

    def update_generate_features_for_lands(self, tags, land_offer):
        feature_list = []
        property_features=land_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(land_offer.property.attributes_object, key) or hasattr(land_offer, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == land_offer.property.attributes_object.subtype:
                                    subtype = {'id': ke, 'value': v}
                                    feature_list.append(subtype)
                if key == 'surface_total' and land_offer.property.attributes_object.surface_total:
                    if land_offer.property.attributes_object.units_of_measure in ['square_meters', 'acres']:
                        surface_field = {'id': value, 'value': int(land_offer.property.attributes_object.surface_total), 'unit': 'ar' }
                    else:
                        surface_field = {'id': value, 'value': int(land_offer.property.attributes_object.surface_total), 'unit': 'ha' }
                    feature_list.append(surface_field)
                if key == 'description_sentimental' and land_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': land_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and land_offer.property.attributes_object.description:
                    description = {'id': value, 'value': land_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and land_offer.price:
                    price = {'id': value, 'value': land_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
                            if feature_list.count({'id': ke, 'value': None}) > 0:
                                feature_list.remove({'id': ke, 'value': None})
                        elif feature.name != va and feature_list.count({'id': ke, 'value': True}) == 0 and feature_list.count({'id': ke, 'value': None}) == 0:
                            ac = {'id': ke, 'value': None}
                            feature_list.append(ac)
        return feature_list

    def generate_features_for_apartments(self, tags, apartment_offer):
        feature_list = []
        property_features=apartment_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(apartment_offer.property.attributes_object, key) or hasattr(apartment_offer.property, key) or hasattr(apartment_offer, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == apartment_offer.property.attributes_object.rental_fund and ke == '852':
                                    built = {'id': ke, 'value': v}
                                    feature_list.append(built)
                                if k == apartment_offer.property.attributes_object.rooms_number and ke == '241':
                                    rooms_number = {'id': ke, 'value': v}
                                    feature_list.append(rooms_number)
                                if k == apartment_offer.property.floor and ke == '248':
                                    floor = {'id': ke, 'value': v}    #"title": "Nivel/Etaj"
                                    feature_list.append(floor)
                                if k == apartment_offer.property.attributes_object.floors and ke == '249':
                                    floors = {'id': ke, 'value': v}    #"title": "Număr de niveluri"
                                    feature_list.append(floors)
                                if k == apartment_offer.property.attributes_object.apartment_construction_material and ke == '247':
                                    apartment_construction_material = {'id': ke, 'value': v}    #"title": "Tip clădire"
                                    feature_list.append(apartment_construction_material)
                                if k == apartment_offer.property.attributes_object.building_plan:
                                    building_plan = {'id': ke, 'value': v}
                                    feature_list.append(building_plan)      
                                if k == apartment_offer.property.attributes_object.apartment_state and ke == '253':
                                    apartment_state = {'id': ke, 'value': v}
                                    feature_list.append(apartment_state)
                                if k == apartment_offer.property.attributes_object.balconies_number and ke == '250':
                                    balconies_number = {'id': ke, 'value': v}
                                    feature_list.append(balconies_number)
                                if k == apartment_offer.property.attributes_object.bathrooms_number and ke == '252':
                                    bathrooms_number = {'id': ke, 'value': v}
                                    feature_list.append(bathrooms_number)
                                if k == apartment_offer.property.attributes_object.garage:
                                    garage = {'id': ke, 'value': v}
                                    feature_list.append(garage)
                                if k == apartment_offer.property.attributes_object.allow_childrens and apartment_offer.type == 'rent':
                                    allow_children = {'id': ke, 'value': v}
                                    feature_list.append(allow_children) 
                                if k == apartment_offer.property.attributes_object.allow_animals and apartment_offer.type == 'rent':
                                    allow_animals = {'id': ke, 'value': v}
                                    feature_list.append(allow_animals) 
                        if va == apartment_offer.property.attributes_object.heating_source:
                            heating_source = {'id': ke, 'value': True} 
                            feature_list.append(heating_source)
                        if va == apartment_offer.property.attributes_object.windows:
                            window = {'id': ke, 'value': True}
                            feature_list.append(window)
                        if va == apartment_offer.property.attributes_object.partitioning:
                            partitioning = {'id': ke, 'value': True}
                            feature_list.append(partitioning)
                if key == 'furnished' and apartment_offer.property.attributes_object.furnished:
                    furnished = {'id': value, 'value': True}
                    feature_list.append(furnished)
                if key == 'surface_total' and apartment_offer.property.attributes_object.surface_total:
                    surface_total = {'id': value, 'value': int(apartment_offer.property.attributes_object.surface_total), 'unit': 'm2'}
                    feature_list.append(surface_total)
                if key == 'surface_util' and apartment_offer.property.attributes_object.surface_util:
                    surface_util = {'id': value, 'value': int(apartment_offer.property.attributes_object.surface_util), 'unit': 'm2'}
                    feature_list.append(surface_util)
                if key == 'surface_kitchen' and apartment_offer.property.attributes_object.surface_kitchen:
                    surface_kitchen = {'id': value, 'value': int(apartment_offer.property.attributes_object.surface_kitchen), 'unit': 'm2'}
                    feature_list.append(surface_kitchen)
                if key == 'ceiling_height' and apartment_offer.property.attributes_object.ceiling_height:
                    ceiling_height = {'id': value, 'value': int(apartment_offer.property.attributes_object.ceiling_height), 'unit': 'cm'}
                    feature_list.append(ceiling_height)
                if key == 'description_sentimental' and apartment_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': apartment_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and apartment_offer.property.attributes_object.description:
                    description = {'id': value, 'value': apartment_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and apartment_offer.price:
                    price = {'id': value, 'value': apartment_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'author':
                for ke, va in value.items():
                    author = {'id': ke, 'value': va}
                    feature_list.append(author)
            if key == 'household_technique':
                for ke, va in value.items():
                    for k, v in va.items():
                        for feature in property_features:
                            if feature.name == k and feature_list.count({'id': '214', 'value': True}) == 0:
                                household = {'id': ke, 'value': True}
                                feature_list.append(household)
            if key == 'anexa':
                for ke, va in value.items():
                    for k, v in va.items():
                        for feature in property_features:
                            if feature.name == k and feature_list.count({'id': '176', 'value': True}) == 0:
                                anexa = {'id': ke, 'value': v}
                                feature_list.append(anexa)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
        return feature_list

    def update_generate_features_for_apartments(self, tags, apartment_offer):
        feature_list = []
        property_features=apartment_offer.property.features.all()
        attr_obj = apartment_offer.property.attributes_object
        prop_obj = apartment_offer.property
        for key, value in tags.items():
            if hasattr(attr_obj, key) or hasattr(apartment_offer.property, key) or hasattr(apartment_offer, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if ke == '852':
                                    if k == attr_obj.rental_fund:
                                        built = {'id': ke, 'value': v}
                                        feature_list.append(built)
                                    elif attr_obj.rental_fund is None:
                                        built = {'id': ke, 'value': None}
                                        feature_list.append(built)
                                if ke == '241':
                                    if k == attr_obj.rooms_number:
                                        rooms_number = {'id': ke, 'value': v}
                                        feature_list.append(rooms_number)
                                    elif attr_obj.rooms_number is None:
                                        rooms_number = {'id': ke, 'value': None}
                                        feature_list.append(rooms_number)
                                if ke == '248':
                                    if k == apartment_offer.property.floor:
                                        floor = {'id': ke, 'value': v}
                                        feature_list.append(floor)
                                    elif prop_obj.floor is None:
                                        floor = {'id': ke, 'value': None}
                                        feature_list.append(floor)
                                if ke == '249':
                                    if k == attr_obj.floors:
                                        floors = {'id': ke, 'value': v}  
                                        feature_list.append(floors)
                                    elif attr_obj.floors is None:
                                        floors = {'id': ke, 'value': None}  
                                        feature_list.append(floors)
                                if ke == '247':
                                    if k == attr_obj.apartment_construction_material:
                                        apartment_construction_material = {'id': ke, 'value': v}   
                                        feature_list.append(apartment_construction_material)
                                    elif attr_obj.apartment_construction_material is None:
                                        apartment_construction_material = {'id': ke, 'value': None}   
                                        feature_list.append(apartment_construction_material)
                                if ke == '246':
                                    if k == attr_obj.building_plan:
                                        building_plan = {'id': ke, 'value': v}
                                        feature_list.append(building_plan) 
                                    elif attr_obj.building_plan is None:
                                        building_plan = {'id': ke, 'value': None}
                                        feature_list.append(building_plan) 
                                if ke == '253':
                                    if k == attr_obj.apartment_state:
                                        apartment_state = {'id': ke, 'value': v}
                                        feature_list.append(apartment_state)
                                    elif attr_obj.apartment_state is None:
                                        apartment_state = {'id': ke, 'value': None}
                                        feature_list.append(apartment_state)
                                if ke == '250' and k == attr_obj.balconies_number:
                                    balconies_number = {'id': ke, 'value': v}
                                    feature_list.append(balconies_number)
                                if ke == '252':
                                    if k == attr_obj.bathrooms_number:
                                        bathrooms_number = {'id': ke, 'value': v}
                                        feature_list.append(bathrooms_number)
                                    elif attr_obj.bathrooms_number is None:
                                        bathrooms_number = {'id': ke, 'value': None}
                                        feature_list.append(bathrooms_number)
                                if ke == '251':
                                    if k == attr_obj.garage:
                                        garage = {'id': ke, 'value': v}
                                        feature_list.append(garage)
                                    if attr_obj.garage is None:
                                        garage = {'id': ke, 'value': None}
                                        feature_list.append(garage)
                                if k == attr_obj.allow_childrens and apartment_offer.type == 'rent':
                                    allow_children = {'id': ke, 'value': v}
                                    feature_list.append(allow_children) 
                                if k == attr_obj.allow_animals and apartment_offer.type == 'rent':
                                    allow_animals = {'id': ke, 'value': v}
                                    feature_list.append(allow_animals) 
                        if key == 'heating_source':
                            if va == attr_obj.heating_source:
                                heating_source = {'id': ke, 'value': True} 
                                feature_list.append(heating_source)
                            elif attr_obj.heating_source is None or attr_obj.heating_source not in ['individual_central_heating', 'underfloor_heating']:
                                heating_source = {'id': ke, 'value': None} 
                                feature_list.append(heating_source)
                        if key == 'windows':
                            if va == attr_obj.windows:
                                window = {'id': ke, 'value': True}
                                feature_list.append(window)
                            elif attr_obj.windows is None or attr_obj.windows != 'double_glazing':
                                window = {'id': ke, 'value': None}
                                feature_list.append(window)
                        if key == 'partitioning':
                            if va == attr_obj.partitioning:
                                partitioning = {'id': ke, 'value': True}
                                feature_list.append(partitioning)
                            elif attr_obj.partitioning is None or attr_obj.partitioning != 'detached':
                                partitioning = {'id': ke, 'value': None} 
                                feature_list.append(partitioning)
                if key == 'furnished':
                    if attr_obj.furnished:
                        furnished = {'id': value, 'value': True}
                        feature_list.append(furnished)
                    elif attr_obj.furnished is None:
                        furnished = {'id': value, 'value': None}
                        feature_list.append(furnished)
                if key == 'surface_total': 
                    if attr_obj.surface_total:
                        surface_total = {'id': value, 'value': int(attr_obj.surface_total), 'unit': 'm2'}
                        feature_list.append(surface_total)
                    elif attr_obj.surface_total is None:
                        surface_total = {'id': value, 'value': None}
                        feature_list.append(surface_total)
                if key == 'surface_util': 
                    if attr_obj.surface_util:
                        surface_util = {'id': value, 'value': int(attr_obj.surface_util), 'unit': 'm2'}
                        feature_list.append(surface_util)
                    elif attr_obj.surface_util is None:
                        surface_util = {'id': value, 'value': None}
                        feature_list.append(surface_util)
                if key == 'surface_kitchen':
                    if attr_obj.surface_kitchen:
                        surface_kitchen = {'id': value, 'value': int(attr_obj.surface_kitchen), 'unit': 'm2'}
                        feature_list.append(surface_kitchen)
                    elif attr_obj.surface_kitchen is None:
                        surface_kitchen = {'id': value, 'value': None}
                        feature_list.append(surface_kitchen)
                if key == 'ceiling_height':  
                    if attr_obj.ceiling_height:
                        ceiling_height = {'id': value, 'value': int(attr_obj.ceiling_height), 'unit': 'cm'}
                        feature_list.append(ceiling_height)
                    elif attr_obj.ceiling_height is None:
                        ceiling_height = {'id': value, 'value': None}
                        feature_list.append(ceiling_height)
                if key == 'description_sentimental':
                    if attr_obj.description_sentimental:
                        title = {'id': value, 'value': attr_obj.description_sentimental}
                        feature_list.append(title)
                    elif attr_obj.description_sentimental is None:
                        title = {'id': value, 'value': None}
                        feature_list.append(title)
                if key == 'description':
                    if attr_obj.description:
                        description = {'id': value, 'value': attr_obj.description}
                        feature_list.append(description)
                    elif attr_obj.description is None:
                        description = {'id': value, 'value': None}
                        feature_list.append(description)
                if key == 'price' and apartment_offer.price:
                    price = {'id': value, 'value': apartment_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'author':
                for ke, va in value.items():
                    author = {'id': ke, 'value': va}
                    feature_list.append(author)
            if key == 'household_technique':
                for ke, va in value.items():
                    for k, v in va.items():
                        for feature in property_features:
                            if feature.name == k and feature_list.count({'id': '214', 'value': True}) == 0:
                                household = {'id': ke, 'value': True}
                                feature_list.append(household)
                                if feature_list.count({'id': '214', 'value': None}) > 0:
                                    feature_list.remove({'id': '214', 'value': None})
                            elif feature.name != k and feature_list.count({'id': '214', 'value': True}) == 0 and feature_list.count({'id': '214', 'value': None}) == 0:
                                household = {'id': ke, 'value': None}
                                feature_list.append(household)
            if key == 'anexa':
                for ke, va in value.items():
                    for k, v in va.items():
                        for feature in property_features:
                            if feature.name == k and feature_list.count({'id': '176', 'value': True}) == 0:
                                anexa = {'id': ke, 'value': v}
                                feature_list.append(anexa)
                                if feature_list.count({'id': '176', 'value': None}) > 0:
                                    feature_list.remove({'id': '176', 'value': None})
                            elif feature.name != k and feature_list.count({'id': '176', 'value': True}) == 0 and feature_list.count({'id': '176', 'value': None}) == 0:
                                anexa = {'id': ke, 'value': None}
                                feature_list.append(anexa)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == va:
                            ac = {'id': ke, 'value': True}
                            feature_list.append(ac)
                            if feature_list.count({'id': ke, 'value': None}) > 0:
                                feature_list.remove({'id': ke, 'value': None})
                        elif feature.name != va and feature_list.count({'id': ke, 'value': True}) == 0 and feature_list.count({'id': ke, 'value': None}) == 0:
                            ac = {'id': ke, 'value': None}
                            feature_list.append(ac)
                        
        return feature_list

    def generate_features_for_houses(self, tags, house_offer):
        feature_list = []
        property_features=house_offer.property.features.all()
        for key, value in tags.items():
            if hasattr(house_offer.property.attributes_object, key) or hasattr(house_offer.property, key) or hasattr(house_offer, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == house_offer.property.attributes_object.subtype and ke == '1311':
                                    subtype = {'id': ke, 'value': v }
                                    feature_list.append(subtype)
                                    
                                if k == house_offer.property.attributes_object.sewerage and ke == '1623':
                                    subtype = {'id': ke, 'value': v }
                                    feature_list.append(subtype)
                                if k == house_offer.property.attributes_object.water_pipes and ke == '1622':
                                    subtype = {'id': ke, 'value': v }
                                    feature_list.append(subtype)
                                if k == house_offer.property.attributes_object.gasification and ke == '1624':
                                    subtype = {'id': ke, 'value': v }
                                    feature_list.append(subtype)
                                    
                                if k == house_offer.property.attributes_object.floors and ke == '249':
                                    floors = {'id': ke, 'value': v }
                                    feature_list.append(floors)
                                if k == house_offer.property.attributes_object.house_state and ke == '254':
                                    house_state = {'id': ke, 'value': v }
                                    feature_list.append(house_state)
                                if k == house_offer.property.attributes_object.house_construction_material and ke == '247':
                                    house_construction_material = {'id': ke, 'value': v }
                                    feature_list.append(house_construction_material)
                                if k == house_offer.property.attributes_object.balconies_number and ke == '250':
                                    balconies_number = {'id': ke, 'value': v}
                                    feature_list.append(balconies_number)
                                if k == house_offer.property.attributes_object.bathrooms_number and ke == '252':
                                    bathrooms_number = {'id': ke, 'value': v}
                                    feature_list.append(bathrooms_number)
                                if k == house_offer.property.attributes_object.allow_childrens and house_offer.type == 'rent':
                                    allow_children = {'id': ke, 'value': v}
                                    feature_list.append(allow_children) 
                                if k == house_offer.property.attributes_object.allow_animals and house_offer.type == 'rent':
                                    allow_animals = {'id': ke, 'value': v}
                                    feature_list.append(allow_animals) 
                        if ke == house_offer.property.attributes_object.windows:
                            window = {'id': va, 'value': True}
                            feature_list.append(window)
                        if ke == house_offer.property.attributes_object.heating_source:
                            heating_source = {'id': va, 'value': True}
                            feature_list.append(heating_source)
                if key == 'rooms_number' and house_offer.property.attributes_object.rooms_number:
                    rooms_number = {'id': value, 'value': house_offer.property.attributes_object.rooms_number} 
                    feature_list.append(rooms_number)
                if key == 'surface_field' and house_offer.property.attributes_object.surface_field:
                    if house_offer.property.attributes_object.units_of_measure in ['square_meters', 'acres']:
                        surface_field = {'id': value, 'value': int(house_offer.property.attributes_object.surface_field), 'unit': 'ar' }
                    else:
                        surface_field = {'id': value, 'value': int(house_offer.property.attributes_object.surface_field), 'unit': 'ha' }
                    feature_list.append(surface_field)
                if key == 'surface_total' and house_offer.property.attributes_object.surface_total:
                    surface_total = {'id': value, 'value': int(house_offer.property.attributes_object.surface_total), 'unit': 'm2' }
                    feature_list.append(surface_total)
                if key == 'surface_kitchen' and house_offer.property.attributes_object.surface_kitchen:
                    surface_kitchen = {'id': value, 'value': int(house_offer.property.attributes_object.surface_kitchen), 'unit': 'm2' }
                    feature_list.append(surface_kitchen)
                if key == 'surface_util' and house_offer.property.attributes_object.surface_util:
                    surface_util = {'id': value, 'value': int(house_offer.property.attributes_object.surface_util), 'unit': 'm2' }
                    feature_list.append(surface_util)
                if key == 'ceiling_height' and house_offer.property.attributes_object.ceiling_height:
                    ceiling_height = {'id': value, 'value': int(house_offer.property.attributes_object.ceiling_height), 'unit': 'cm' }
                    feature_list.append(ceiling_height)
                if key == 'furnished' and house_offer.property.attributes_object.furnished:
                    furnished = {'id': value, 'value': True}
                    feature_list.append(furnished)
                if key == 'garage' and house_offer.property.attributes_object.garage:
                    garage = {'id': value, 'value': True}
                    feature_list.append(garage)
                if key == 'description_sentimental' and house_offer.property.attributes_object.description_sentimental:
                    title = {'id': value, 'value': house_offer.property.attributes_object.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and house_offer.property.attributes_object.description:
                    description = {'id': value, 'value': house_offer.property.attributes_object.description}
                    feature_list.append(description)
                if key == 'price' and house_offer.price:
                    price = {'id': value, 'value': house_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            if key == 'author':
                for ke, va in value.items():
                    author = {'id': ke, 'value': va}
                    feature_list.append(author)
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == ke:
                            check_box = {'id': va, 'value': True}
                            feature_list.append(check_box)
            if key == 'household_technique':
                for ke, va in value.items():
                    for k, v in va.items():
                        for feature in property_features:
                            if feature.name == k and feature_list.count({'id': '214', 'value': True}) == 0:
                                household = {'id': ke, 'value': v}
                                feature_list.append(household)
        return feature_list
        
    def update_generate_features_for_houses(self, tags, house_offer):
        feature_list = []
        property_features=house_offer.property.features.all()
        attr_obj = house_offer.property.attributes_object
        for key, value in tags.items():
            if hasattr(attr_obj, key) or hasattr(house_offer.property, key) or hasattr(house_offer, key):
                if type(value) is dict:
                    for ke, va in value.items():
                        if type(va) is dict:
                            for k, v in va.items():
                                if k == attr_obj.subtype and ke == '1311':
                                    subtype = {'id': ke, 'value': v }
                                    feature_list.append(subtype)
                                if k == attr_obj.floors and ke == '249':
                                    floors = {'id': ke, 'value': v }
                                    feature_list.append(floors)
                                if k == attr_obj.house_state and ke == '254':
                                    house_state = {'id': ke, 'value': v }
                                    feature_list.append(house_state)
                                if k == attr_obj.house_construction_material and ke == '247':
                                    house_construction_material = {'id': ke, 'value': v }
                                    feature_list.append(house_construction_material)
                                if k == attr_obj.balconies_number and ke == '250':
                                    balconies_number = {'id': ke, 'value': v}
                                    feature_list.append(balconies_number)
                                if k == attr_obj.bathrooms_number and ke == '252':
                                    bathrooms_number = {'id': ke, 'value': v}
                                    feature_list.append(bathrooms_number)
                                if k == attr_obj.allow_childrens and house_offer.type == 'rent':
                                    allow_children = {'id': ke, 'value': v}
                                    feature_list.append(allow_children) 
                                if k == attr_obj.allow_animals and house_offer.type == 'rent':
                                    allow_animals = {'id': ke, 'value': v}
                                    feature_list.append(allow_animals)
                        if key == 'windows':
                            if ke == attr_obj.windows:
                                window = {'id': va, 'value': True}
                                feature_list.append(window)
                            elif attr_obj.windows != ke:
                                window = {'id': va, 'value': None}
                                feature_list.append(window)
                        if key == 'heating_source':
                            if ke == attr_obj.heating_source:
                                heating_source = {'id': va, 'value': True}
                                feature_list.append(heating_source)
                            elif attr_obj.heating_source not in ['individual_central_heating', 'underfloor_heating']:
                                heating_source = {'id': va, 'value': None}
                                feature_list.append(heating_source)
                if key == 'ceiling_height' :
                    if attr_obj.ceiling_height:
                        ceiling_height = {'id': value, 'value': int(attr_obj.ceiling_height)} 
                        feature_list.append(ceiling_height)
                    elif attr_obj.ceiling_height is None:
                        ceiling_height = {'id': value, 'value': None} 
                        feature_list.append(ceiling_height)
                if key == 'rooms_number' and attr_obj.rooms_number:
                    rooms_number = {'id': value, 'value': int(attr_obj.rooms_number)} 
                    feature_list.append(rooms_number)
                if key == 'surface_field' and attr_obj.surface_field:
                    if attr_obj.units_of_measure in ['square_meters', 'acres']:
                        surface_field = {'id': value, 'value': int(attr_obj.surface_field), 'unit': 'ar' }
                    else:
                        surface_field = {'id': value, 'value': int(attr_obj.surface_field), 'unit': 'ha' }
                    feature_list.append(surface_field)
                if key == 'surface_total' and attr_obj.surface_total:
                    surface_total = {'id': value, 'value': int(attr_obj.surface_total), 'unit': 'm2' }
                    feature_list.append(surface_total)
                if key == 'surface_util' and attr_obj.surface_util:
                    surface_util = {'id': value, 'value': int(attr_obj.surface_util), 'unit': 'm2' }
                    feature_list.append(surface_util)
                if key == 'furnished':
                    if attr_obj.furnished:
                        furnished = {'id': value, 'value': True}
                        feature_list.append(furnished)
                    elif attr_obj.furnished is None:
                        furnished = {'id': value, 'value': None}
                        feature_list.append(furnished)
                if key == 'garage': 
                    if attr_obj.garage:
                        garage = {'id': value, 'value': True}
                        feature_list.append(garage)
                    elif attr_obj.garage is None:
                        garage = {'id': value, 'value': None}
                        feature_list.append(garage)
                if key == 'description_sentimental' and attr_obj.description_sentimental:
                    title = {'id': value, 'value': attr_obj.description_sentimental}
                    feature_list.append(title)
                if key == 'description' and attr_obj.description:
                    description = {'id': value, 'value': attr_obj.description}
                    feature_list.append(description)
                if key == 'price' and house_offer.price:
                    price = {'id': value, 'value': house_offer.price, 'unit': 'eur'}
                    feature_list.append(price)
            
            if key == 'check_box_features':
                for ke, va in value.items():
                    for feature in property_features:
                        if feature.name == ke and feature_list.count({'id': va, 'value': True}) == 0:
                            check_box = {'id': va, 'value': True}
                            feature_list.append(check_box)
                            if feature_list.count({'id': va, 'value': None}) > 0:
                                feature_list.remove({'id': va, 'value': None})
                        elif feature.name != va and feature_list.count({'id': va, 'value': True}) == 0 and feature_list.count({'id': va, 'value': None}) == 0:
                            check_box = {'id': va, 'value': None}
                            feature_list.append(check_box)
            if key == 'household_technique':
                for ke, va in value.items():
                    for k, v in va.items():
                        for feature in property_features:
                            if feature.name == k and feature_list.count({'id': '214', 'value': True}) == 0:
                                household = {'id': ke, 'value': True}
                                feature_list.append(household)
                                if feature_list.count({'id': '214', 'value': None}) > 0:
                                    feature_list.remove({'id': '214', 'value': None})
                            elif feature.name != k and feature_list.count({'id': '214', 'value': True}) == 0 and feature_list.count({'id': '214', 'value': None}) == 0:
                                household = {'id': ke, 'value': None}
                                feature_list.append(household)
            
        return feature_list


    def image_upload_999(self, offer):
        if offer.property.user.premium_999:
            images = offer.property.images.filter(hide_on_site=False)
        elif not offer.property.user.premium_999:
            images = offer.property.images.filter(hide_on_site=False)
        imges_ids = []

        for img in images:
            url_img = get_details_medium_watermarked_thumbnail_url(img.image_path)
            response = requests.get(url_img)
            files = {'file': response.content,
                    'Content-Type': 'image/jpeg'}
            url_image_upload = self.generate_url_999(self.UPLOAD_IMAGES)
            response = self.send_request_999(url=url_image_upload, username=offer.property.user.token_999, files=files, type_request='IMAGE_POST')
            message = f'STATUS CODE (999.md) - {response.status_code}' + f' RESPONSE - {response.text}'
            if 200 <= response.status_code < 300:
                response_json = response.json()
                imges_ids.append(response_json['image_id'])
                rollbar.report_message(message="Image was uploaded succesfully!", level='info')
            elif 300 <= response.status_code < 400:
                rollbar.report_message(message=message, level='warning')
            elif response.status_code >= 400:
                rollbar.report_message(message=message, level='error')
        return imges_ids

    def create_advert_999(self, offer):
        # generate json
        json_dict = {}
        hdr = {}
        header = self.generate_headers_999(hdr)
        json_dict['category_id'] = '270'
        self.generate_json_data_tags_999(json_dict, self.SUBCATEGORIES, offer)
        self.generate_json_data_tags_999(json_dict, self.OFFER_TYPES, offer)
        common_feature_list = self.generate_common_features(self.COMMON_FEATURES, offer)
        images_ids = self.image_upload_999(offer)
        if len(images_ids) > 0: 
            if offer.property.type == 'apartment':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                apartment_feature_list = self.generate_features_for_apartments(self.APARTMENT_FEATURES, offer)
                feature_list = apartment_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.CREATE_ADVERT)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='POST')
            elif offer.property.type == 'house':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                house_feature_list = self.generate_features_for_houses(self.HOUSE_FEATURES, offer)
                feature_list = house_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.CREATE_ADVERT)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='POST')
            elif offer.property.type == 'land':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                land_feature_list = self.generate_features_for_lands(self.LAND_FEATURES, offer)
                feature_list = land_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.CREATE_ADVERT)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='POST')
            elif offer.property.type in ['basement_parking', 'garage']:
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                gp_feature_list = self.generate_features_for_lands(self.GARAGE_PARKING_FEATURES, offer)
                feature_list = gp_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.CREATE_ADVERT)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='POST')
            elif offer.property.type == 'commercial':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                commercial_feature_list = self.generate_features_for_commercial_space(self.COMMERCIAL_FEATURES, offer)
                feature_list = commercial_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.CREATE_ADVERT)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='POST')
        if 200 <= response.status_code < 300:
            offer.mls_999_data['is_created'] = True 
            offer.advert_id_999 = response.json()['advert']['id']
            offer.save()

    def update_advert_999(self, offer):
        json_dict = {}
        hdr = {}
        header = self.generate_headers_999(hdr)
        common_feature_list = self.generate_common_features(self.COMMON_FEATURES, offer)
        images_ids = self.image_upload_999(offer)
        if len(images_ids) > 0:  
            if offer.property.type == 'apartment':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                apartment_feature_list = self.update_generate_features_for_apartments(self.APARTMENT_FEATURES, offer)
                feature_list = apartment_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.UPDATE_ADVERT, offer.advert_id_999)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='PATCH')
            elif offer.property.type == 'house':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids]}]
                house_feature_list = self.update_generate_features_for_houses(self.HOUSE_FEATURES, offer)
                feature_list = house_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.UPDATE_ADVERT, offer.advert_id_999)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='PATCH')
            elif offer.property.type == 'land':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                land_feature_list = self.update_generate_features_for_lands(self.LAND_FEATURES, offer)
                feature_list = land_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.UPDATE_ADVERT, offer.advert_id_999)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='PATCH')
            elif offer.property.type in ['basement_parking', 'garage']:
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                gp_feature_list = self.update_generate_features_for_garage_and_parking(self.GARAGE_PARKING_FEATURES, offer)
                feature_list = gp_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.UPDATE_ADVERT, offer.advert_id_999)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='PATCH')
            elif offer.property.type == 'commercial':
                images_list = [{ 'id':'14', 'value':[img for img in images_ids] }]
                commercial_feature_list = self.update_generate_features_for_commercial_space(self.COMMERCIAL_FEATURES, offer)
                feature_list = commercial_feature_list + common_feature_list + images_list
                json_dict['features'] = feature_list
                url = self.generate_url_999(self.UPDATE_ADVERT, offer.advert_id_999)
                json_obj = json.dumps(json_dict)
                response = self.send_request_999(url=url, username=offer.property.user.token_999, headers=header, json=json_obj, type_request='PATCH')
        if 200 <= response.status_code < 300:
            offer.mls_999_data['is_updated'] = True
            offer.save()
                
            
                
        
        
            

        
        



        