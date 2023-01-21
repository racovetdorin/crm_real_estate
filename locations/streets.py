import requests
import json
from time import sleep
from difflib import SequenceMatcher
from datetime import datetime
from langdetect import detect
import rollbar

from .models import *

# response = requests.get(url=url, auth=(username, password), data=json, headers=headers)


def get_streets(url, username, password, headers):
    response = requests.get(url=url, auth=(username, password), headers=headers)
    if response.status_code != 200:
        print('response status code', response.status_code)
        print('sleep for 10 sec')
        sleep(10)
        print('retry call ---------------------- ')
        response = requests.get(url=url, auth=(username, password), headers=headers)
        print('Now should be ok ------- ')
        if response.status_code != 200:
            print('response status code', response.status_code)
            print('sleep second time for 10 sec')
            sleep(10)
            print('retry call ---------------------- ')
            response = requests.get(url=url, auth=(username, password), headers=headers)
            print('Now should be ok ------- ')

    return json.loads(response.text)


def get_request(city_name, q):
    base_url = "https://map.md/api/companies/webmap/search_street?location=" + city_name + "&q=" + q
    return get_streets(base_url, '2c3e340b-88ad-40c2-888a-f112fd58af59', '', {'Content-type': 'application/json;'})

def get_str(id, nr, location):
    url = f"https://map.md/api/companies/webmap/get_street?id={id}&location={location}&number={nr}"
    return get_streets(url, '2c3e340b-88ad-40c2-888a-f112fd58af59', '', {'Content-type': 'application/json;'})
    


def get_all_street():
    import string
    start_msg = ('Start time = ' ,datetime.now().strftime("%H:%M:%S"))
    rollbar.report_message(message=start_msg, level='info')
    sleep(10)
    for city in City.objects.filter(name__isnull=False):
        for i in string.ascii_lowercase:
            resp = get_request(city.name, i)
            if resp != []:
                for r in resp:
                    lang = detect(r['name'])
                    if 'centroid' in r.keys():
                        
                        if lang == 'ro':
                            street, created_str = Street.objects.get_or_create(name=r['name'], id_999=int(r['id']), city=city, latitude=r['centroid']['lat'], longitude=r['centroid']['lon'])
                        elif lang == 'ru':
                            if 'tags' in r.keys():
                                for t in r['tags']:
                                    if detect(t) == 'ro':
                                        street, created_str = Street.objects.get_or_create(name=t, id_999=int(r['id']), city=city, latitude=r['centroid']['lat'], longitude=r['centroid']['lon'])
                                        
                    else:
                        if lang == 'ro':
                            street, created_str = Street.objects.get_or_create(name=r['name'], id_999=int(r['id']), city=city)
                        elif lang == 'ru':
                            if 'tags' in r.keys():
                                for t in r['tags']:
                                    if detect(t) == 'ro':
                                        street, created_str = Street.objects.get_or_create(name=t, id_999=int(r['id']), city=city)
                    if created_str:
                        if SequenceMatcher(None, city.name, r['parent_name']).ratio() > 0.75:
                            if r['buildings'] != []:
                                for number in r['buildings']:
                                    rs = get_str(r['id'], number, city.name)
                                    if rs != []:
                                        str_number, created_str_nr = StreetNumber.objects.get_or_create(number=number, street=street, latitude=rs['point']['lat'], longitude=rs['point']['lon'])
    end_msg = ('End Time = ' ,datetime.now().strftime("%H:%M:%S"))
    rollbar.report_message(message=end_msg, level='info')


            