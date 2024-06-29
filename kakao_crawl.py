#####Driver code for crawling address data from Kakaotalk group chat(PC), conversion into excel/csv########import pywinauto
# Imports
import pywinauto
import datetime
from pywinauto.application import Application as app
from pywinauto import clipboard
from pywinauto import keyboard
import time
import os
import pandas as pd
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import googlemaps
from functools import partial
import requests

#############################################################################################################
# 카카오톡 프로그램 경로
path = "C:\\Program Files (x86)\\Kakao\\KakaoTalk\\KakaoTalk.exe"
tgtwindow = "용인시 공유전동킥보드 불법주차 신고"
kwrd = "용인시"
# 카카오톡 기록 저장 경로
filepath = 'C:\\Users\\user\\OneDrive\\문서\\카카오톡 받은 파일'

# setting up for kakao app
kakao_setup = app('uia').start(path)
kakao = app('uia').connect(path=path)

# 프로세스들 찾기 finding all available processes
procs = pywinauto.findwindows.find_elements()


def save_to_txt():
    for proc in procs:
        # print("Current process:", proc.name)
        # print(proc)
        if kwrd in proc.name:
            print(f'keword {kwrd} found')
            chat = app('win32').connect(title=proc.name)
            print("chat selected and connected")
            chat_dlg = chat[tgtwindow]
            chat_dlg.print_control_identifiers()
            # print("windows:", chat.windows())

            # 카카오톡 내보내기 기능 사용
            # To save as txt file invoking kakao chat export function
            chat_dlg.Edit.click()
            chat_dlg.type_keys('^s')
            time.sleep(1)
            save_dlg = pywinauto.Desktop(backend="win32").window(title_re='.*다른 이름으로 저장*', found_index=0)

            # 파일이름 지정: 24시간에 한번 수집하기 때문에 년월일로 저장
            # Since we will collect data every 24hrs, use current YYYY-MM-DD format as filename
            current_time = datetime.datetime.now()
            txt_filename = str(current_time).split(" ")[0] + "_logs"
            save_dlg.set_focus()
            save_dlg.Edit.set_text(txt_filename)

            # 엔터 눌러 저장하기
            # Hitting Enter key to save
            save_dlg.type_keys('{ENTER}')
            time.sleep(1)

            # 다음 저장을 위해 확인 화면 꺼주기
            # To close the confirmation window
            time.sleep(2)
            keyboard.send_keys('{ENTER}')

            return txt_filename


# 저장된 카카오 채팅 기록 열기
# Function to open and read saved log file
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

    return addresses
    # date_address_pairs = list(zip(dates, addresses))
    #
    # for pair in date_address_pairs:
    #     print(pair)


######################################GEOCODING FUNCTIONS-USE AS DESIRED#############################################

# Using google maps API(paid account)
def geocoding_gmap(address):
    # import googlemaps
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


# Using kakao API(rate limited)
def geocoding_kakao(address):
    url = 'https://dapi.kakao.com/v2/local/search/address'
    auth = {'Authorization': 'KakaoAK ${REST_API_KEY}'}
    query = {'query': f'{address}'}
    try:
        res = requests.get(url, auth, query).json()
        lon, lat = res[0]['documents']['x'], res[0]['documents']['y']  # 경도, 위도 순으로 나타남
        return lat, lon  # 위도경도 순으로 리턴하기
    except:
        print("This request cannot be processed by the server, please try again")
        return 0, 0


##################################################################################################################

# now need to see pandas working to see if as expected


# Driver code
def main():
    current = save_to_txt()
    current_filepath = os.path.join(filepath, f'{current}.txt')

    chat = read_chat_history(current_filepath)
    addresses = extract_addresses(chat)

    data = []
    for address in addresses:
        lat, lon = geocoding_geopy(address)
        data.append({'address': address, 'latitude': lat, 'longitude': lon})

    res = pd.DataFrame(data)

    csv_filename = os.path.join(filepath, 'address_geocoded.csv')
    res.to_csv(csv_filename, index=True, index_label="index")
    print(f"Geocoded csv {csv_filename} completed")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60*60*24)
