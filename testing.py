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
#import googlemaps
from functools import partial
import requests


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
    locs = geocode_result[0]['geometry']['locations'] #{'lat' : x, 'lng' : y}
    return locs

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
    # return loc.longitude, loc.latitude, address

#Using kakao API(rate limited)
def geocoding_kakao(address):
    



chatrec = read_chat_history(fullpath)
addresses = extract_addresses(chatrec)
locex = geocoding_geopy("성복 2로 86")

#https://velog.io/@s0young/Troubleshooting-GeoPy%EC%9D%98-geocoding-%EC%B2%98%EB%A6%AC-%EC%86%8D%EB%8F%84%EB%8A%94-%EC%99%9C-%EB%8A%90%EB%A6%B4%EA%B9%8C
# https://m.blog.naver.com/rackhunson/222403071709
