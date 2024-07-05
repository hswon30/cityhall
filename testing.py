import pywinauto
import datetime
from pywinauto.application import Application as app
from pywinauto import clipboard
from pywinauto import keyboard
import time
import os
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import googlemaps
from functools import partial
import requests
import json
import pandas as pd


filepath = 'C:\\Users\\user\\Downloads\\Telegram Desktop'
name = '2024-06-26_log.txt'
fullpath = os.path.join(filepath, name)

print(fullpath)

def read_chat_history(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        print(f'{filename}, found')
        return file.read()


def extract_addresses(chat_history):
    # Define regex patterns for addresses and dates
    address_pattern = re.compile(r'\[.*?\] \[.*?\] - (.*?)\n', re.MULTILINE)

    address_patterns = [
        r'\[.*?\] \[.*?\] 1\.\s*(.*)',
        r'\[.*?\] \[.*?\] -\s*(.*)',
        r'\[.*?\] \[.*?\] 위반장소 -\s*(.*)',
        r'\[.*?\] \[.*?\] 1\.\위반장소\s*\-\s*(.*)'
        r'\[.*?\] \[.*?\] -\s*\위반장소\s*\-\s*(.*)'
    ]

    date_pattern = re.compile(r'--------------- (\d{4}년 \d{1,2}월 \d{1,2}일 .*?) ---------------')

    # dates = date_pattern.findall(chat_history)

    addresses = []
    for pattern in address_patterns:
        matches = re.findall(pattern, chat_history, re.MULTILINE)
        addresses.extend(matches)

    for address in addresses:
        print(address)
    return addresses
    # date_address_pairs = list(zip(dates, addresses))
    #
    # for pair in date_address_pairs:
    #     print(pair)


# Using google maps API(paid account)
def geocoding_gmap(address):
    #import googlemaps
    gmaps = googlemaps.Client(key='Your_API_Key')
    geocode_result = gmaps.geocode(address)

    # {'lat' : x, 'lng' : y}
    lat = geocode_result[0]['geometry']['locations']['lat']
    lng = geocode_result[0]['geometry']['locations']['lon']
    return lat, lng

# Using free geopy(limited functionality)
def geocoding_geopy(address):
    # print(address)
    geolocator = Nominatim(user_agent="South Korea")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    loc = geocode(address, language='KOR')
    if loc:
        print(f"location {address} found")
        # print(f'log: {loc.longitude}, lat: {loc.latitude}, addr: {address}')
        return loc.latitude, loc.longitude
    else:
        print(f"unable to code location: {address}")
        return 0, 0
    # return loc.longitude, loc.latitude, address

#Using kakao API(rate limited)
def geocoding_kakao(address):
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
    auth = {'Authorization': 'KakaoAK 83ca70aa0cffa452d24e6706d0389b73'}
    # query = {'query': f'{address}'}
    try:
        time.sleep(1)
        res = requests.get(url, headers=auth).json()
        print("kakao query processed")
        lon, lat = res['documents'][0]['x'], res['documents'][0]['y']
        return lat, lon

        # print(f'address: {address} found: lat{lat}, lon{lon}')
        # return lat, lon #위도경도 순으로 리턴하기
    except:
        print(f"This {address} request cannot be processed by the server, please try again")
        return 0, 0

geocoding_kakao("수지구 수지로124성복스퀘어입니다")
geocoding_kakao("처인구 금학로 241번길")


# chat = read_chat_history(fullpath)
# addresses = extract_addresses(chat)
#
# data = []
# for address in addresses:
#     lat, lon = geocoding_kakao(address)
#     data.append({'address': address, 'latitude': lat, 'longitude': lon})
#
# res = pd.DataFrame(data)
#
# res.head(10)
#
# csv_filename = 'geocoding_sample_2.csv'
# res.to_csv(csv_filename, index=True, index_label="index")
# print(f"Geocoded csv {csv_filename} completed")

#https://velog.io/@s0young/Troubleshooting-GeoPy%EC%9D%98-geocoding-%EC%B2%98%EB%A6%AC-%EC%86%8D%EB%8F%84%EB%8A%94-%EC%99%9C-%EB%8A%90%EB%A6%B4%EA%B9%8C
# https://m.blog.naver.com/rackhunson/222403071709


address_patterns = [
    r'\[.*?\] \[.*?\] 1\.\s*(.*)',
    r'\[.*?\] \[.*?\] -\s*(.*)',
    r'\[.*?\] \[.*?\] 위반장소 -\s*(.*)',
    r'\[.*?\] \[.*?\] 1\.위반장소\s*-\s*(.*)',
    r'\[.*?\] \[.*?\] -\s*위반장소\s*-\s*(.*)',
]

refine_pattern = r'([^\(]+)'


chat_history = read_chat_history(fullpath)

addresses = []

for line in chat_history.strip().split('\n'):
    for pattern in address_patterns:
        match = re.search(pattern, line)
        if match:
            address = match.group(1).strip()
            refined_match = re.search(refine_pattern, address)
            if refined_match:
                address = refined_match.group(1).strip()
                cleaned_address = address.replace("위반장소 -", "").strip()
                addresses.append(cleaned_address)
                print(f'matching line is : {line}')
                break


for address in addresses:
    print(f"Extracted address: {address}")