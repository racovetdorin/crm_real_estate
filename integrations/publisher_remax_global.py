from email import header
from math import degrees
import uuid
from datetime import datetime
import logging.config
from crm.filters import get_details_medium_watermarked_thumbnail_url
from offices.models import Office
from .models import Integration
import json
import requests
import logging
from properties.models import Property, PropertyImage, BasePropertyAttributes
from offers.models import Offer
from users.models import User, UserImage
import rollbar
from decouple import config

# import urllib2


logger = logging.getLogger(__name__)


class BaseHandlerREXAPI(object):
    BASE_URL = config('BASE_GLOBAL_URL')
    BASE_VALIDATE_URL = config('BASE_GLOBAL_VALIDATE_URL')
    BASE_IMAGE_URL = 'https://media.rmx.casa'

    API_KEY = 'api_key='
    TOKEN_AUTH = 'OAUTH oauth_token='

    JSON_OFFICE_ORDERED_TAGS = ['Address1', 'Address2', 'CityID', 'CollectionCertified', 'CommercialCertified',
                                'Disabled', 'Email', 'Fax',
                                'ImageFileName', 'IntegratorID', 'IntegratorOfficeID', 'IsRegionalOffice', 'Latitude',
                                'LeadAdminAgentID', 'LocalZoneID', 'Longitude', 'MacroOfficeID', 'MarketingInfo',
                                'OfficeName',
                                'OfficePassword', 'OfficeUserID', 'OfficeUserIDDisabled', 'Phone', 'PostalCode',
                                'ProcessImage', 'Redirects',
                                'RegionID', 'RemoveImage', 'ShowAgentDirectDial', 'SucceedCertified', 'URLToPrivatePage'
                                ]

    INTEGRATOR_DATA_TAG = {
        'IntegratorOfficeID': 'integrator_id',
    }

    PROPERTY_DATA_TAGS_MAPPING_REXAPI = {
        'house': 2,  # 2 for residential according to documentation
        'apartment': 2,
        'studio': 2,
        'commercial': 1,  # 1 for commercial according to documentation
        'land': 2,
        'hotel': 1,
        'cabin': 2,
        'complex': 2,
        'basement_parking': 2,
        'garage': 1,
        'storage_room': 1,
        'active': 160,
        'transacted': 169,
        'sale': 261,
        'rent': 260,
        1: 333,
        2: 336,
        3: 337,
        4: 338,
        5: 339,
        6: 340,
        7: 341,
        8: 342,
        9: 343,
        10: 335
    }

    PROPERTY_DATA_TAGS_MAPPING_PROPERTY_TYPE = {
        'house': 202,  # 2 for residential according to documentation
        'apartment': 194,
        'studio': 1009,
        'commercial_space': 13,
        'industrial_space': 16,
        'office_space': 20,
        'basement_parking': 2806,
        'land': 211,
        'hotel': 1114,
        'cabin': 195,
        'garage': 15,
        'storage_room': 3213,
        'commercial': 1
    }

    CREATE_OFFICE, UPDATE_OFFICE, GET_OFFICE, GET_OFFICES, CANCEL_OFFICE = 'create_office', 'update_office', 'get_office', 'get_offices', 'cancel_office'
    CREATE_AGENT, UPDATE_AGENT, GET_AGENT, GET_AGENTS, CANCEL_AGENT = 'create_agent', 'update_agent', 'get_agent', 'get_agents', 'cancel_agent'
    CREATE_PROPERTY, UPDATE_PROPERTY, GET_PROPERTY, GET_PROPERTIES, DELETE_PROPERTY = 'create_property', 'update_property', 'get_property', 'get_properties', 'delete_property'
    GET_DESCRIPTION = 'get_description'
    CREATE_DESCRIPTION_PROPERTY, UPDATE_DESCRIPTION_PROPERTY = 'create_description', 'update_description'
    CREATE_IMAGE_PROPERTY, UPDATE_IMAGE_PROPERTY, DELETE_IMAGES_PROPERTY, DELETE_ONE_IMAGE_PROPERTY, GET_IMAGES_PROPERTY = 'create_image_property', 'update_image_property', 'delete_images_property', 'delete_one_image_property', 'get_images_property'
    CANCEL_OFFICE_EXTERNALID, CANCEL_AGENT_EXTERNALID, CANCEL_PROPERTY_EXTERNALID = 'cancel_office_externalid', 'cancel_agent_externalid', 'cancel_property_externalid'

    GEO_DATA = {
        'CityID': 'city_gobal_id',
    }

    GEO_DATA_COORDINATES = {
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    }

    @classmethod
    def generate_json_data_tags(cls, dict_json, tags, object):
        for key, value in tags.items():
            if hasattr(object, value):
                object_attr = getattr(object, value)

                if isinstance(object, Property) or isinstance(object, Offer):
                    if object_attr in cls.PROPERTY_DATA_TAGS_MAPPING_REXAPI.keys():
                        dict_json[key] = cls.PROPERTY_DATA_TAGS_MAPPING_REXAPI[object_attr]
                    if object_attr in cls.PROPERTY_DATA_TAGS_MAPPING_PROPERTY_TYPE.keys():
                        if not dict_json.get(key) or key == 'PropertyType':
                            if object_attr == 'commercial':
                                dict_json[key] = cls.PROPERTY_DATA_TAGS_MAPPING_PROPERTY_TYPE[
                                    object.attributes_object.subtype]
                            else:
                                dict_json[key] = cls.PROPERTY_DATA_TAGS_MAPPING_PROPERTY_TYPE[object_attr]
                    else:
                        dict_json[key] = object_attr

                elif isinstance(object, UserImage):
                    if key == "ImageURL":
                        dict_json[key] = cls.BASE_IMAGE_URL + f"/{getattr(object, value)}"
                    else:
                        dict_json[key] = object_attr

                elif isinstance(object, PropertyImage):
                    if key == "ImageURL":
                        img_url = getattr(object, value)
                        dict_json[key] = get_details_medium_watermarked_thumbnail_url(img_url)
                    else:
                        dict_json[key] = object_attr

                elif isinstance(object, User):
                    if key == "AgentName":
                        object_attr = object.first_name + ' ' + object.last_name
                        dict_json[key] = object_attr
                    else:
                        dict_json[key] = object_attr
                else:
                    dict_json[key] = object_attr

    @classmethod
    def generate_geo_coordinates_json(cls, dict_json, tags, object):
        geo_coordinates = {}
        for key, value in tags.items():
            if hasattr(object, value):
                geo_coordinates[key] = getattr(object, value)
        dict_json['GeoCoordinates'] = geo_coordinates

    @classmethod
    def generate_geo_data_json(cls, dict_json, tags, object):
        geo_data = {}
        for key, value in tags.items():
            if getattr(object, value):
                city_object = getattr(object, value)
                geo_data[key] = city_object.rex_id
        dict_json['GeoData'] = geo_data

    @classmethod
    def generate_mandatory_tags(cls, dict_json, tags, object):
        for key, value in tags.items():
            if getattr(object, value):
                dict_json[key] = getattr(object, value)

    @classmethod
    def generate_url(cls, integration_object, type_url, object=None, page=1, size=100,
                     english=False, image_id=None):
        id_integrator = getattr(integration_object, 'integrator_id')
        base_integrator_url = cls.BASE_URL + '/integrator/' + f'{id_integrator}'
        if id_integrator:
            # URLs for offices
            if type_url == cls.CREATE_OFFICE:
                return base_integrator_url + '/offices'
            elif type_url == cls.GET_OFFICE and object != None:
                return base_integrator_url + '/offices/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.CANCEL_OFFICE and object != None:
                return base_integrator_url + '/offices/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.CANCEL_OFFICE_EXTERNALID:
                return base_integrator_url + '/offices/' + f'ext-{object}'
            elif type_url == cls.GET_OFFICES:
                return base_integrator_url + f'/offices?page={page}&take={size}'

            # URLs for agents
            elif type_url == cls.CREATE_AGENT:
                return base_integrator_url + '/associates'
            elif type_url == cls.GET_AGENT and object != None:
                return base_integrator_url + '/associate/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.GET_AGENTS:
                return base_integrator_url + '/associates?page=' + f'{page}' + '&take=' + f'{size}'
            elif type_url == cls.UPDATE_AGENT and object != None:
                return base_integrator_url + '/associates/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.CANCEL_AGENT and object != None:
                return base_integrator_url + '/associates/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.CANCEL_AGENT_EXTERNALID:
                return base_integrator_url + '/associates/' + f'ext-{object}'
            elif type_url == cls.CREATE_PROPERTY:
                return base_integrator_url + '/properties'
            elif type_url == cls.CREATE_DESCRIPTION_PROPERTY and object != None:
                return base_integrator_url + '/propertydescriptions/' + f'ext-{object.external_id.strip()}'  # property external ID

            # URLs for property
            elif type_url == cls.GET_PROPERTY and object != None:
                return base_integrator_url + '/properties/' + f'ext-{object.external_id.strip()}'  # property external ID
            elif type_url == cls.GET_PROPERTIES:
                return base_integrator_url + '/properties/' + f'?page={page}&take={size}'  # property external ID
            elif type_url == cls.UPDATE_OFFICE and object != None:
                return base_integrator_url + '/offices/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.UPDATE_PROPERTY and object != None:
                return base_integrator_url + '/properties/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.DELETE_PROPERTY and object != None:
                return base_integrator_url + '/properties/' + f'ext-{object.external_id.strip()}/' + 'cancel'
            elif type_url == cls.CREATE_IMAGE_PROPERTY and object != None:
                return base_integrator_url + '/propertyImages/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.GET_IMAGES_PROPERTY and object != None:
                return base_integrator_url + '/propertyImages/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.GET_DESCRIPTION and object != None:
                return base_integrator_url + '/propertydescriptions/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.UPDATE_DESCRIPTION_PROPERTY and object != None:
                return base_integrator_url + '/propertydescriptions/' + f'ext-{object.external_id.strip()}' + f'' \
                                                                                                              f'/{629}/{"ENG" if english else "ROM"}'
            elif type_url == cls.UPDATE_IMAGE_PROPERTY and object != None and image_id != None:
                return base_integrator_url + '/propertyImages/' + f'ext-{object.external_id.strip()}/' + image_id
            elif type_url == cls.CANCEL_PROPERTY_EXTERNALID:
                return base_integrator_url + '/properties/' + f'ext-{object}/' + 'cancel'
            elif type_url == cls.DELETE_IMAGES_PROPERTY and object != None:
                return base_integrator_url + '/propertyImages/' + f'ext-{object.external_id.strip()}'
            elif type_url == cls.DELETE_ONE_IMAGE_PROPERTY and object != None:
                if isinstance(object, PropertyImage):
                    return base_integrator_url + '/propertyImages/' + f'ext-{object.property.offer.external_id.strip()}/' \
                           + f'{image_id}'
                else:
                    return base_integrator_url + '/propertyImages/' + f'ext-{object.external_id.strip()}/' + f'{image_id}'

        logger.error("Id generator couldn't be created!")
        rollbar.report_message("Id generator couldn't be created!")
        raise Exception("Error: id generator couldn't be created")

    @classmethod
    def generate_headers(cls, dict_headers, integration_object):
        accept = 'application/json; charset=utf-8'
        content_type = 'application/json; charset=utf-8'
        token = integration_object.refresh_token
        key = integration_object.api_key
        dict_headers['Authorization'] = cls.TOKEN_AUTH + f'"{token}"' + ', ' + cls.API_KEY + f'"{key}"'
        dict_headers['Accept'] = accept
        dict_headers['Content-type'] = content_type

    @classmethod
    def is_valid_token(cls):
        integration_object = Integration.objects.get(name='rex')
        token = integration_object.refresh_token
        if token is None:
            cls.generate_token(integration_object)
            integration_object = Integration.objects.get(name='rex')
            return integration_object
        token = requests.utils.quote(token)
        key = integration_object.api_key
        id_integrator = integration_object.integrator_id
        hdrs = {}
        cls.generate_headers(hdrs, integration_object)
        url = cls.BASE_VALIDATE_URL + r'/ValidateToken?' + f'apiKey={key}&' + f'token={token}&' + f'integratorID={id_integrator}'
        response = requests.post(url=url, headers=hdrs)
        message = f'STATUS CODE - {response.status_code}' + f' RESPONSE - {response.text}'
        if 200 <= response.status_code < 300:
            response_dict = response.json()
            if response_dict['tokenstatus'] == 'Valid':
                logger.info("Token Valid")
                rollbar.report_message(message="Token valid!", level='info')
            elif response_dict['tokenstatus'] == 'Expired' or response_dict['tokenstatus'] == 'Invalid':
                logger.warning("Token invalid")
                rollbar.report_message(message="Token expired/invalid", level='warning')
                cls.generate_token(integration_object)
                integration_object = Integration.objects.get(name='rex')
                logger.info("Token was generated")
                rollbar.report_message(message="The token has been generated!", level='info')
        elif response.status_code >= 300:
            logger.error(message)
            rollbar.report_message(message=message, level=40)
        return integration_object

    @classmethod
    def send_request(cls, url, headers, json=None, type_request=None):
        response = ''
        if type_request == 'POST':
            response = requests.post(url=url, data=json, headers=headers)
        elif type_request == 'GET':
            response = requests.get(url=url, data=json, headers=headers)
        elif type_request == 'PUT':
            response = requests.put(url=url, data=json, headers=headers)
        elif type_request == 'PATCH':
            response = requests.patch(url=url, data=json, headers=headers)
        elif type_request == 'DELETE':
            response = requests.delete(url=url, data=json, headers=headers)

        message = f'STATUS CODE - {response.status_code}' + f' RESPONSE - {response.text}'

        if 200 <= response.status_code < 300:
            logger.info(message)
            rollbar.report_message(message=message, level='info')
        elif 300 <= response.status_code < 400:
            logger.warning(message)
            rollbar.report_message(message=message, level='warning')
        elif response.status_code >= 400:
            logger.error(message)
            rollbar.report_message(message=message, level='error')
        return response

    @classmethod
    def generate_token(cls, integration_object):
        dict_headers = {}
        dict_body = {}
        token_url = cls.BASE_URL + '/oauth/token'
        body = f'grant_type=authorization_code&client_id={integration_object.api_key}&code={integration_object.secret_key}'
        dict_headers['Accept'] = 'application/json; charset=utf-8'
        dict_headers['Content-type'] = 'application/x-www-form-urlencoded'
        dict_body[''] = body
        response = cls.send_request(token_url, dict_headers, dict_body, 'POST')
        if 200 <= response.status_code < 300:
            status_code = response.status_code
            response = json.loads(response.text)
            integration_object.refresh_token = response['access_token']
            integration_object.save()
            logger.info(f'{status_code} - S-a generat token-ul!')
            rollbar.report_message(message=f'{status_code} - S-a generat token-ul!', level='info')
        elif 300 <= response.status_code:
            logger.error(f'A aparut o eroare la generarea token ului!')
            rollbar.report_message(message='An error has occurred while generating the token', level='error')


class REXOfficesHandlerAPI(BaseHandlerREXAPI):
    OFFICE_DATA_TAGS = {
        'ExternalID': 'external_id',
        'InternationalID': 'international_id',
        'OfficeName': 'name',
        'Address1': 'address',
        'PostalCode': 'postal_code',
        'Email': 'email',
        'Phone': 'phone_1',
        'URLToPrivatePage': 'office_url',
        'ImageURL': 'office_image_url',
        'OfficeDescription': 'office_description'
    }

    def __init__(self):
        super(BaseHandlerREXAPI, self).__init__()

    def create_offices(self, office):
        """
        Function responsible to send a POST request with offices in order to list them on Global
        """
        integrationObject = self.is_valid_token()
        json_dict = {}
        headers = {}
        self.generate_headers(headers, integrationObject)
        self.generate_json_data_tags(json_dict, self.OFFICE_DATA_TAGS, office)
        self.generate_geo_data_json(json_dict, self.GEO_DATA, office)
        self.generate_geo_coordinates_json(json_dict, self.GEO_DATA_COORDINATES, office)
        json_file = json.dumps(json_dict)
        url = self.generate_url(integrationObject, self.CREATE_OFFICE)
        self.send_request(url=url, json=json_file, headers=headers, type_request='POST')

    def get_office(self, office):
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        url = self.generate_url(integration_object=integrationObject, type_url=self.GET_OFFICE, object=office, )
        self.send_request(url=url, headers=headers, type_request='GET')

    def update_office(self, office):
        integrationObject = self.is_valid_token()
        json_dict = {}
        headers = {}
        self.generate_headers(headers, integrationObject)
        self.generate_json_data_tags(json_dict, self.OFFICE_DATA_TAGS, office)
        self.generate_geo_data_json(json_dict, self.GEO_DATA, office)
        self.generate_geo_coordinates_json(json_dict, self.GEO_DATA_COORDINATES, office)
        json_file = json.dumps(json_dict)
        url = self.generate_url(integrationObject, self.UPDATE_OFFICE, object=office)
        self.send_request(url=url, json=json_file, headers=headers, type_request='PUT')

    def cancel_office(self, office):
        integrationObject = self.is_valid_token()
        json_dict = {}
        headers = {}
        self.generate_headers(headers, integrationObject)
        json_dict['Terminated'] = True
        json_file = json.dumps(json_dict)
        if isinstance(office, Office):
            url = self.generate_url(integrationObject, self.CANCEL_OFFICE, object=office)
        else:
            url = self.generate_url(integrationObject, self.CANCEL_OFFICE_EXTERNALID, object=office)
        self.send_request(url=url, json=json_file, headers=headers, type_request='PATCH')

    def get_offices(self):
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        url = self.generate_url(integration_object=integrationObject, type_url=self.GET_OFFICES)
        return self.send_request(url=url, headers=headers, type_request='GET')

    def delete_all_listed_offices(self):
        offices = self.get_offices().json()
        for office in offices['Items']:
            self.cancel_office(office['ExternalID'])


class REXAgentsHandlerAPI(BaseHandlerREXAPI):
    AGENTS_DATA_OFFICE = {
        'OfficeExternalID': 'office'
    }

    AGENTS_DATA_TAGS = {
        'AgentName': 'display_title',
        'ExternalID': 'external_id',
        'InternationalID': 'international_id',
        'FirstName': 'first_name',
        'LastName': 'last_name',
        'Email': 'email',
        'Phone': 'phone',
        'URLToPrivatePage': 'agent_url',
        'IsSalesAssociate': 'is_sale_associate',
        'MainSpecialization': 'specialization',
        'Closer': 'user_description'
    }

    AGENT_DATE_JOINED_REMAX = {
        'DateJoinedREMAX': 'date_joined'
    }
    AGENT_IMAGE = {
        'ImageURL': 'image_path'
    }

    def __init__(self):
        super(BaseHandlerREXAPI, self).__init__()

    @classmethod
    def generate_date_joined(cls, dict_json, agent_tags, agent):
        for key, value in agent_tags.items():
            if getattr(agent, value):
                x = getattr(agent, value).date()
                x = x.__str__()
                dict_json[key] = x

    @classmethod
    def generate_agents_office_json(cls, dict_json, agent_tags, agent):
        for key, value in agent_tags.items():
            if getattr(agent, value):
                office_object = getattr(agent, value)
                dict_json[key] = office_object.external_id

    @classmethod
    def generate_region_id(cls, dict_headers, integration_object):
        dict_headers['RegionID'] = integration_object.region_id

    @classmethod
    def generate_header_agent_update(cls, dict_headers, integration_object):
        accept = 'application/json; charset=utf-8 ation/json; charset=utf-8'
        content_type = 'application/json; charset=utf-8'
        token = integration_object.refresh_token
        key = integration_object.api_key
        dict_headers['Authorization'] = cls.TOKEN_AUTH + f'"{token}"' + ', ' + cls.API_KEY + f'"{key}"'
        dict_headers['Accept'] = accept
        dict_headers['Content-type'] = content_type

    def get_agents(self):
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(headers, integrationObject)
        url = self.generate_url(integrationObject, self.GET_AGENTS)
        return self.send_request(url=url, headers=headers, type_request='GET')

    def create_agent(self, agent):
        integrationObject = self.is_valid_token()
        user_image = UserImage.objects.filter(user=agent).first()
        json_dict = {}
        headers = {}
        self.generate_headers(headers, integrationObject)
        self.generate_region_id(json_dict, integrationObject)
        self.generate_agents_office_json(json_dict, self.AGENTS_DATA_OFFICE, agent)
        self.generate_json_data_tags(json_dict, self.AGENTS_DATA_TAGS, agent)
        self.generate_date_joined(json_dict, self.AGENT_DATE_JOINED_REMAX, agent)
        self.generate_json_data_tags(json_dict, self.AGENT_IMAGE, user_image)
        json_file = json.dumps(json_dict)
        url = self.generate_url(integrationObject, 'create_agent')
        self.send_request(url=url, json=json_file, headers=headers, type_request='POST')

    def get_agent(self, agent):
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        url = self.generate_url(integration_object=integrationObject, type_url=self.GET_AGENT, object=agent)
        self.send_request(url=url, headers=headers, type_request='GET')

    def update_agent(self, agent):
        integrationObject = self.is_valid_token()
        user_image = UserImage.objects.filter(user=agent).first()
        json_dict = {}
        headers = {}
        self.generate_header_agent_update(headers, integrationObject)
        self.generate_region_id(json_dict, integrationObject)
        self.generate_agents_office_json(json_dict, self.AGENTS_DATA_OFFICE, agent)
        self.generate_json_data_tags(json_dict, self.AGENTS_DATA_TAGS, agent)
        self.generate_date_joined(json_dict, self.AGENT_DATE_JOINED_REMAX, agent)
        self.generate_json_data_tags(json_dict, self.AGENT_IMAGE, user_image)
        json_file = json.dumps(json_dict)
        url = self.generate_url(integrationObject, self.UPDATE_AGENT, object=agent)
        self.send_request(url=url, json=json_file, headers=headers, type_request='PUT')

    def cancel_agent(self, agent):
        integrationObject = self.is_valid_token()
        json_dict = {}
        headers = {}
        self.generate_header_agent_update(headers, integrationObject)
        json_dict['Terminated'] = True
        json_file = json.dumps(json_dict)
        if isinstance(agent, User):
            url = self.generate_url(integrationObject, self.CANCEL_AGENT, object=agent)
        else:
            url = self.generate_url(integrationObject, self.CANCEL_AGENT_EXTERNALID, object=agent)
        self.send_request(url=url, json=json_file, headers=headers, type_request='PATCH')

    def cancel_agents_using_externalID(self):
        agents = self.get_agents().json()
        for agent in agents['Items']:
            self.cancel_agent(agent['ExternalID'])


class REXPropertiesHandlerAPI(BaseHandlerREXAPI):
    GEO_DATA_PROPERTIES = {
        'CityID': 'city'
    }

    PROPERTY_DESCRIPTION_TAGS = {
        'DescriptionText': 'attributes_object',
        'LanguageCode': 'ROM',
        'DescriptionType': 629,
    }

    PROPERTY_IMAGES_TAGS = {
        'ImageURL': 'image_path'
    }

    PROPERTY_DATA_TAGS = {
        'CommercialResidential': 'type',  # property
        'VirtualTourURL': 'virtual_tour',
        'PropertyType': 'attributes_object',
        'StreetNumber': 'street_number',
        'StreetName': 'street',
        'ApartmentNumber': 'apartment_number',
    }

    PROPERTY_OFFER_DATA_TAGS = {
        'CurrentListingPrice': 'price',
        'TransactionType': 'type',  # offers
        'ListingStatus': 'status',  # offers
        'ExternalID': 'external_id',
    }

    PROPERTY_ASSCOCIATE_ID = {
        'AssociateExternalID': 'user'
    }

    DICT_CONSTANT_PROPERTY_DATA_TAGS = {
        'CurrentListingCurrency': 'EUR',
        'PropertyStatus': 190,
        'AlternateURL': 'https://remax.md/details/'
    }

    PROPERTY_ATTRIBUTES_TAGS = {
        'TotalArea': 'surface_total',
        'BuiltArea': 'surface_built',
        'LivingArea': 'surface_built',
        'TotalNumOfRooms': 'rooms_number',
        'YearBuilt': 'construction_year',
        'NumberOfBathrooms': 'bathrooms_number',
        'NumberOfToiletRooms': 'bathrooms_number',
        'NumberOfApartmentsInBuilding': 'floors',
        'FloorLevel': 'floors',
        'NumberOfBedrooms': 'rooms_number',
        'ParkingSpaces': 'garage',
        'LotSizeM2': 'surface_total'
    }

    DEFAULT_DICT = {
        "CubicVolume": int(3.14159265358979),
        "HeatingCost": int(3.14159265358979),
        'Energy': {
            "IncludesEnergyForWarmWater": 1,
            "ElectricityConsumption": int(3),
            "ElectricityConsumptionUOM": 3299,
            "EnergyCertificateType": 3491,
            "EnergyPerformance": int(3),
            "EnergyCertificateDate": "1967-08-13",
            "EnergyPerformanceUOM": 3299,
            "EnergyRating": 2842,
            "EnergyRatingValue": 5,
            "EnergyRatingNotes": "String"
        },
        "HeatingCostPeriod": 2008,
        "LotSize": "String",
        "MaintenanceFee": 3,
        "MaintenanceFeePeriod": 2008,
        "Notes": "String",
        "ParkingCost": 3,
        "ParkingCostPeriod": 2008,
        "RentalCommissionMonths": "String",
        "Utilities": 3,
        "UtilityPeriod": 2008,
    }

    def __init__(self):
        super(BaseHandlerREXAPI, self).__init__()

    def generate_property_data_tags(self, property, json):
        for key, value in self.PROPERTY_DATA_TAGS.items():
            if hasattr(property, value):
                attr = getattr(property, value)
                if key == 'CommercialResidential':
                    json[key] = self.PROPERTY_DATA_TAGS_MAPPING_REXAPI[attr]
                elif key == 'PropertyType' and property.type == 'commercial':
                    json[key] = self.PROPERTY_DATA_TAGS_MAPPING_PROPERTY_TYPE[property.attributes_object.subtype]
                elif key == 'PropertyType':
                    json[key] = self.PROPERTY_DATA_TAGS_MAPPING_PROPERTY_TYPE[property.type]
                elif key == 'StreetName':
                    if property.street:
                        json[key] = property.street.name
                else:
                    json[key] = attr

    def generate_property_attributes_tags(self, property, json):

        for key, value in self.PROPERTY_ATTRIBUTES_TAGS.items():
            if hasattr(property.attributes_object, value):
                attr = getattr(property.attributes_object, value)
                if not attr:
                    continue
                if key == 'TotalNumOfRooms':
                    number_of_bedrooms = 0
                    if property.attributes_object.rooms_number:
                        number_of_bedrooms += property.attributes_object.rooms_number
                    if property.attributes_object.kitchens_number:
                        number_of_bedrooms += property.attributes_object.kitchens_number
                    if property.attributes_object.bathrooms_number:
                        number_of_bedrooms += property.attributes_object.bathrooms_number

                    if number_of_bedrooms == 0:
                        continue
                    attr = number_of_bedrooms
                elif key in ['NumberOfBathrooms', 'NumberOfToiletRooms', 'NumberOfApartmentsInBuilding']:
                    if not attr:
                        attr = 0
                elif key == 'ParkingSpaces':
                    if property.attributes_object.garage is not None:
                        attr = 1
                        json['Features'] = '21,'
                    else:
                        continue
                elif key == 'EnergyRating':
                    attr = 2842  # A class
                elif key == 'FloorLevel':
                    if attr:
                        if attr > 9:
                            attr = self.PROPERTY_DATA_TAGS_MAPPING_REXAPI[10]
                        elif isinstance(attr, int):
                            attr = self.PROPERTY_DATA_TAGS_MAPPING_REXAPI[attr]
                        else:
                            attr = self.PROPERTY_DATA_TAGS_MAPPING_REXAPI[1]
                    else:
                        continue
                elif key in ['LotSizeM2', 'BuiltArea', 'LivingArea', 'TotalArea']:
                    if BasePropertyAttributes.UnitsOfMeasure.values[1] == property.attributes_object.units_of_measure:
                        # conversion acres to square meters
                        attr = int(attr * 4.047)
                    elif BasePropertyAttributes.UnitsOfMeasure.values[2] == property.attributes_object.units_of_measure:
                        # conversion hectares to square meters
                        attr = int(attr * 10000)
                    elif not property.attributes_object.units_of_measure:
                        continue
                    else:
                        attr = int(attr)
                elif isinstance(attr, float):
                    if not attr:
                        continue
                    attr = int(attr)

                json[key] = attr


    def generate_default_tags(self, dict_json):
        for key, value in self.DEFAULT_DICT.items():
            dict_json[key] = value

    def generate_property_offer_data_tags(self, offer, json):
        for key, value in self.PROPERTY_OFFER_DATA_TAGS.items():
            if hasattr(offer, value):
                atr = getattr(offer, value)
                if atr in self.PROPERTY_DATA_TAGS_MAPPING_REXAPI.keys():
                    json[key] = self.PROPERTY_DATA_TAGS_MAPPING_REXAPI[atr]
                else:
                    json[key] = atr

    @staticmethod
    def is_valid_offer(offer):
        if offer is None:
            return False
        if not offer.mls_remax_global:
            return False
        elif offer.status in ['incomplete', 'withdrawn', 'pending', 'reserved']:
            return False
        elif not offer.promote_site:
            return False
        elif not offer.property.city.rex_id:
            return False
        return True

    def generate_associate_property_tag(self, dict_json, tags, object):
        for key, value in tags.items():
            if getattr(object, value):
                agent = getattr(object, value)
                dict_json[key] = agent.external_id

    def generate_constant_data_tags_for_property(self, dict_json, tags):
        for key, value in tags.items():
            dict_json[key] = value

    def generate_image_property(self, image, integration_object, sequence_number, offer):
        headers = {}
        self.generate_headers(headers, integration_object)
        dict_json = {}
        self.generate_json_data_tags(dict_json, self.PROPERTY_IMAGES_TAGS, image)
        dict_json['SequenceNumber'] = sequence_number
        json_file = json.dumps(dict_json)
        url = self.generate_url(integration_object, self.CREATE_IMAGE_PROPERTY, offer)
        json_response = self.send_request(url=url, json=json_file, headers=headers, type_request='POST')
        if 200 <= json_response.status_code < 300:
            image.rex_ids[offer.external_id] = str(json_response.json()['ID'])
            image.save()
        return json_response

    def get_all_images_property(self, integration_object, offer):
        headers = {}
        self.generate_headers(headers, integration_object)
        url = self.generate_url(integration_object, self.GET_IMAGES_PROPERTY, offer)
        json_response = self.send_request(url=url, headers=headers, type_request='GET')
        return json_response

    def general_update_image_property(self, integration_object, property, offer):
        # Ar trebui verificata stergerea imaginilor
        """
        1. Facem get pe imaginile proprietatii
        2. Verificam lungimea listei de imagini returnata comparand-o cu lista de img de pe baza noastra de date
        3. Daca lung listei de pe global e mai mare decat lung listei bazei noastre de date:
            - identificam imgainea si o stergem de pe global   
        """
        # image_property_list = PropertyImage.objects.filter(property=property).exclude(hide_on_site=True, rex_id=None)
        # image_property_list = [ imagini listate pe global ]
        image_property = PropertyImage.objects.filter(property=property)
        image_property_list = [image for image in image_property
                               if not (image.rex_ids.get(offer.external_id) is None and
                                       image.hide_on_site is True)]
        get_images = self.get_all_images_property(integration_object, offer)
        if not (200 <= get_images.status_code < 300):
            return get_images.status_code
        json_images_list = get_images.json()
        if json_images_list['TotalCount'] > len(image_property_list):
            json_image_list_dict = {}
            for image in json_images_list['Items']:
                json_image_list_dict[str(image['ID'])] = 0
            for image in image_property_list:
                matching_image_id = image.rex_ids.get(offer.external_id)
                if matching_image_id in json_image_list_dict:
                    json_image_list_dict[matching_image_id] += 1
            for key, value in json_image_list_dict.items():
                if value == 0:
                    response = self.delete_one_image_property(offer, image_id=key)
                    if not (200 <= response.status_code < 300):
                        return response.status_code
        image_fail_to_create = []
        if len(image_property_list) > 0:
            sequence_number = 1
            headers = {}
            self.generate_headers(headers, integration_object)
            for image in image_property_list:
                # verificam hide_on_site
                if image.hide_on_site is True and image.rex_ids.get(offer.external_id) is not None:
                    # imaginea a fost urcata pe global
                    response = self.delete_one_image_property(offer, image,
                                                              image_id=str(image.rex_ids[offer.external_id]))
                    if not (200 <= response.status_code < 300):
                        return response.status_code
                elif not image.rex_ids.get(offer.external_id):
                    response = self.generate_image_property(image, integration_object, sequence_number, offer)
                    if response.status_code == 400 and response.json().get('MessageDetail') is not None:
                        if response.json()['MessageDetail'].find('SequenceNumber error') != -1:
                            image_fail_to_create.append((sequence_number, image))
                    elif 300 <= response.status_code:
                        return response.status_code
                    sequence_number += 1
                else:
                    response = self.update_image_property(image, sequence_number, offer)
                    if not (200 <= response.status_code < 300):
                        return response.status_code
                    sequence_number += 1
            # Verificam imaginile care nu s-au creat 
            if len(image_fail_to_create) > 0:
                for image in image_fail_to_create:
                    response = self.generate_image_property(image[1], integration_object, image[0], offer)
                    if not (200 <= response.status_code < 300):
                        return response.status_code

    def update_image_property(self, image, id, offer):
        headers = {}
        integrationObject = self.is_valid_token()
        self.generate_headers(headers, integrationObject)
        dict_json = {}
        self.generate_json_data_tags(dict_json, self.PROPERTY_IMAGES_TAGS, image)
        dict_json['SequenceNumber'] = id
        json_file = json.dumps(dict_json)
        url = self.generate_url(integrationObject, self.UPDATE_IMAGE_PROPERTY, offer,
                                image_id=image.rex_ids[offer.external_id])
        response = self.send_request(url=url, json=json_file, headers=headers, type_request='PUT')
        return response

    def delete_images_property(self, property):
        image_property_list = PropertyImage.objects.filter(property=property)
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(headers, integrationObject)
        if len(image_property_list) > 0:
            url = self.generate_url(integrationObject, self.DELETE_IMAGES_PROPERTY, property)
            response = self.send_request(url=url, headers=headers, type_request='DELETE')
            if 200 <= response.status_code < 300:
                for image in image_property_list:
                    image.rex_id = None
                    image.save()

    def delete_one_image_property(self, offer, image=None, image_id=None):
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(headers, integrationObject)
        if image is None:
            url = self.generate_url(integrationObject, self.DELETE_ONE_IMAGE_PROPERTY, object=offer, image_id=image_id)
        else:
            url = self.generate_url(integrationObject, self.DELETE_ONE_IMAGE_PROPERTY, object=offer,
                                    image_id=image.rex_ids.get(offer.external_id))
        response = self.send_request(url=url, headers=headers, type_request='DELETE')
        if 200 <= response.status_code < 300 and image:
            del image.rex_ids[offer.external_id]
            image.save()
        return response

    def create_description_property(self, dict_json, tags, property, english=False):
        for key, value in tags.items():
            if hasattr(property, str(value)):
                attribute_object = getattr(property, value)
                if not english:
                    dict_json[key] = attribute_object.description
                else:
                    dict_json[key] = attribute_object.description_english
            else:
                if english and key == 'LanguageCode':
                    dict_json[key] = 'ENG'
                else:
                    dict_json[key] = value
        dict_json['PropertyExternalID'] = property.external_id

    def create_property(self, property, offer):
        response_property, response_rom_description, response_eng_description, response_create_image = None, None, None, None
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        dict_json_property = {}
        dict_json_description_ro = {}
        self.generate_property_data_tags(json=dict_json_property, property=property)
        self.generate_property_offer_data_tags(json=dict_json_property, offer=offer)
        self.generate_associate_property_tag(dict_json=dict_json_property, tags=self.PROPERTY_ASSCOCIATE_ID,
                                             object=offer)
        self.generate_constant_data_tags_for_property(dict_json=dict_json_property,
                                                      tags=self.DICT_CONSTANT_PROPERTY_DATA_TAGS)
        self.generate_geo_coordinates_json(dict_json=dict_json_property, tags=self.GEO_DATA_COORDINATES,
                                           object=property)
        self.generate_geo_data_json(dict_json=dict_json_property, tags=self.GEO_DATA_PROPERTIES,
                                    object=property)
        self.generate_property_attributes_tags(json=dict_json_property, property=property)
        dict_json_property['ContractType'] = 25
        dict_json_property['AlternateURL'] += str(offer.id)

        self.create_description_property(dict_json=dict_json_description_ro, property=property,
                                         tags=self.PROPERTY_DESCRIPTION_TAGS)

        url_property = self.generate_url(integration_object=integrationObject, type_url=self.CREATE_PROPERTY)

        url_description_property = self.generate_url(integration_object=integrationObject,
                                                     type_url=self.CREATE_DESCRIPTION_PROPERTY,
                                                     object=offer)

        dict_json = json.dumps(dict_json_property)
        dict_json_description_ro = json.dumps(dict_json_description_ro)

        response_property = self.send_request(url=url_property, json=dict_json, headers=headers, type_request='POST')
        response_rom_description = self.send_request(url=url_description_property, json=dict_json_description_ro,
                                                     headers=headers,
                                                     type_request='POST')
        if property.attributes_object.description_english:
            dict_json_description_en = {}
            self.create_description_property(dict_json=dict_json_description_en, property=property,
                                             tags=self.PROPERTY_DESCRIPTION_TAGS, english=True)
            dict_json_description_en = json.dumps(dict_json_description_en)
            response_eng_description = self.send_request(url=url_description_property, json=dict_json_description_en,
                                                         headers=headers,
                                                         type_request='POST')
        if 200 <= response_property.status_code < 300:
            response_create_image = self.general_update_image_property(integrationObject, property, offer)
        return response_property, response_rom_description, response_eng_description, response_create_image

    def update_property(self, property, offer):
        response_property, response_rom_description, response_eng_description, response_update_image = None, None, None, None
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        dict_json_property = {}
        dict_json_description_ro = {}
        self.generate_property_data_tags(json=dict_json_property, property=property)
        self.generate_property_offer_data_tags(json=dict_json_property, offer=offer)
        self.generate_associate_property_tag(dict_json=dict_json_property, tags=self.PROPERTY_ASSCOCIATE_ID,
                                             object=offer)
        self.generate_constant_data_tags_for_property(dict_json=dict_json_property,
                                                      tags=self.DICT_CONSTANT_PROPERTY_DATA_TAGS)
        self.generate_geo_coordinates_json(dict_json=dict_json_property, tags=self.GEO_DATA_COORDINATES,
                                           object=property)
        self.generate_geo_data_json(dict_json=dict_json_property, tags=self.GEO_DATA_PROPERTIES,
                                    object=property)
        self.generate_property_attributes_tags(json=dict_json_property, property=property)
        dict_json_property['ContractType'] = 25
        dict_json_property['AlternateURL'] += str(offer.id)
        self.create_description_property(dict_json=dict_json_description_ro, property=property,
                                         tags=self.PROPERTY_DESCRIPTION_TAGS)

        url_property = self.generate_url(integration_object=integrationObject, type_url=self.UPDATE_PROPERTY,
                                         object=offer)

        url_description_property = self.generate_url(integration_object=integrationObject,
                                                     type_url=self.UPDATE_DESCRIPTION_PROPERTY,
                                                     object=offer)

        dict_json = json.dumps(dict_json_property)
        dict_json_description_ro = json.dumps(dict_json_description_ro)

        response_property = self.send_request(url=url_property, json=dict_json, headers=headers, type_request='PUT')
        response_rom_description = self.send_request(url=url_description_property, json=dict_json_description_ro,
                                                     headers=headers, type_request='PUT')
        if property.attributes_object.description_english:
            dict_json_description_en = {}
            self.create_description_property(dict_json=dict_json_description_en, property=property,
                                             tags=self.PROPERTY_DESCRIPTION_TAGS, english=True)
            dict_json_description_en = json.dumps(dict_json_description_en)
            url_description_property_eng = self.generate_url(integration_object=integrationObject,
                                                             type_url=self.UPDATE_DESCRIPTION_PROPERTY,
                                                             object=offer, english=True)
            response_eng_description = self.send_request(url=url_description_property_eng,  json=dict_json_description_en,
                                                         headers=headers, type_request='PUT')
        response_update_image = self.general_update_image_property(integrationObject, property, offer)
        return response_property, response_rom_description, response_eng_description, response_update_image

    def cancel_listing(self, offer, property=None):
        integrationObject = self.is_valid_token()
        if isinstance(offer, Offer):
            url = self.generate_url(integration_object=integrationObject, object=offer,
                                    type_url=self.DELETE_PROPERTY)
        else:
            url = self.generate_url(integration_object=integrationObject, object=offer,
                                    type_url=self.CANCEL_PROPERTY_EXTERNALID)
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        response = self.send_request(url=url, headers=headers, type_request='PUT')
        if not (200 <= response.status_code < 300):
            return response
        if not isinstance(offer, Offer):
            try:
                offer = Offer.objects.get(external_id=offer)
            except Offer.DoesNotExist:
                rollbar.report_message(message="Offer.DoesNotExist: 875 ( caz exceptional )", level='error')
                return response
        images = PropertyImage.objects.filter(property=property)
        if len(images) > 0:
            for image in images:
                del image.rex_ids[offer.external_id]
                image.save()
        offer.mls_remax_global_data = {}
        offer.external_id = str(uuid.uuid4())
        offer.save()
        return response

    def get_properties(self):
        integrationObject = self.is_valid_token()
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        url = self.generate_url(integration_object=integrationObject, type_url=self.GET_PROPERTIES)
        return self.send_request(url=url, headers=headers, type_request='GET')

    def modify_listed_properies(self):
        properties = self.get_properties().json()
        for property in properties['Items']:
            p = Property.objects.filter(external_id=property['ExternalID'])
            if len(p) == 0:
                self.cancel_listing(property['ExternalID'])
            else:
                offer = Offer.objects.filter(property=p.first()).first()
                property['is_created'] = True
                if offer is not None:
                    offer.mls_remax_global_data = property
                    offer.save()

    def get_description(self, offer):
        integrationObject = Integration.objects.get(name='rex')
        headers = {}
        self.generate_headers(dict_headers=headers, integration_object=integrationObject)
        url = self.generate_url(integration_object=integrationObject,
                                type_url=self.GET_DESCRIPTION, object=offer)
        self.send_request(url=url, headers=headers, type_request='GET')

    def cancel_properties_using_externalID(self):
        properties = self.get_properties().json()
        for p in properties['Items']:
            self.cancel_listing(p['ExternalID'])

    @staticmethod
    def generate_uuid_offers():
        offers = Offer.objects.all()
        for offer in offers:
            offer.external_id = uuid.uuid4()
            offer.save()

    @staticmethod
    def migrate_external_id_from_image_to_json():
        images = PropertyImage.objects.filter(rex_id__isnull=False)
        for image in images:
            image.rex_ids[image.property.external_id] = image.rex_id
            image.save()
        images = PropertyImage.objects.filter(rex_id__isnull=False)
        for image in images:
            if image.rex_ids[image.property.external_id] != image.rex_id:
                rollbar.report_message(
                    message=f"Error: Failed to migrate image rex ids for {image}, prop: {image.property.external_id}",
                    level='error')

        rollbar.report_message(
            message=f"INFO: Successful migration of rex id for images",
            level='info')

    def migrate_external_id_from_property_to_offer(self):
        properties = self.get_properties().json()
        for p in properties['Items']:
            try:
                property = Property.objects.filter(external_id=p['ExternalID'])
                if len(property) > 1:
                    rollbar.report_message(
                        message=f"Error: More properties than one {len(property)} : property object externalID {p['ExternalID']},"
                                f" {p['AlternateURL']}", level='error')
                    continue
                property = property.first()
                offer = Offer.objects.filter(property=property)
                if len(offer) > 1:
                    rollbar.report_message(
                        message=f"Error: more offers than 1 for object externalID {p['ExternalID']}, {p['AlternateURL']}",
                        level='error')
                    continue
                offer = offer.first()
                offer.external_id = property.external_id
                offer.save()
            except Property.DoesNotExist:
                rollbar.report_message(message=f"Error: property object externalID {p['ExternalID']},"
                                               f" {p['AlternateURL']}", level='error')
        for p in properties['Items']:
            try:
                property = Property.objects.filter(external_id=p['ExternalID'])
                if len(property) > 1:
                    rollbar.report_message(
                        message=f"Error: More properties than one {len(property)} : property object externalID {p['ExternalID']},"
                                f" {p['AlternateURL']}", level='error')
                    continue
                property = property.first()
                offer = Offer.objects.filter(property=property)
                if len(offer) > 1:
                    rollbar.report_message(
                        message=f"Error (checking now): more offers than 1 for object externalID {p['ExternalID']}, {p['AlternateURL']}",
                        level='error')
                    continue
                offer = offer.first()
                if offer.external_id != property.external_id:
                    rollbar.report_message(
                        message=f"Error (migratin images rex_ids - checcking): Failed to migrate for {property.external_id}, "
                                f"{p['AlternateURL']}",
                        level='error')
            except Property.DoesNotExist:
                pass
