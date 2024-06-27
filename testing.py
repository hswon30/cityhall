import pywinauto
import datetime
from pywinauto.application import Application as app
from pywinauto import clipboard
from pywinauto import keyboard
import time
import os
import re

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
        r'\[.*?\] \[.*?\] 1\.\s*(.*)',  # Matches '1. address'
        r'\[.*?\] \[.*?\] -\s*(.*)',  # Matches '- address'
        r'\[.*?\] \[.*?\] 위반장소 -\s*(.*)',
        r'\[.*?\] \[.*?\] 1\.\위반장소\s*\-\s*(.*)'
        r'\[.*?\] \[.*?\] -\s*\위반장소\s*\-\s*(.*)'# Matches '위반장소 - address'
    ]

    date_pattern = re.compile(r'--------------- (\d{4}년 \d{1,2}월 \d{1,2}일 .*?) ---------------')

    dates = date_pattern.findall(chat_history)

    addresses = []
    for pattern in address_patterns:
        matches = re.findall(pattern, chat_history, re.MULTILINE)
        addresses.extend(matches)

    for address in addresses:
        print(address)
    # date_address_pairs = list(zip(dates, addresses))
    #
    # for pair in date_address_pairs:
    #     print(pair)


chatrec = read_chat_history(fullpath)
extract_addresses(chatrec)


#https://velog.io/@s0young/Troubleshooting-GeoPy%EC%9D%98-geocoding-%EC%B2%98%EB%A6%AC-%EC%86%8D%EB%8F%84%EB%8A%94-%EC%99%9C-%EB%8A%90%EB%A6%B4%EA%B9%8C


