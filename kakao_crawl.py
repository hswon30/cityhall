#####Driver code for crawling address data from Kakaotalk group chat(PC), conversion into excel/csv########import pywinauto
#Imports
import pywinauto
import datetime
from pywinauto.application import Application as app
from pywinauto import clipboard
from pywinauto import keyboard
import time
import os
import pandas as pd
#############################################################################################################

path = "C:\\Program Files (x86)\\Kakao\\KakaoTalk\\KakaoTalk.exe"
tgtwindow = "용인시 공유전동킥보드 불법주차 신고"
kwrd = "용인시"
filepath = 'C:\\Users\\user\\OneDrive\\문서\\카카오톡 받은 파일\\'


#setting up for kakao app
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
            txt_filename = str(current_time).split(" ")[0]+"_logs"
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
def read_txt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()



# Driver code
def main():
    current = save_to_txt()
    current_filepath = os.path.join(filepath, current)

