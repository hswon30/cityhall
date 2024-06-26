#####Driver code for crawling address data from Kakaotalk group chat(PC), conversion into excel/csv########import pywinauto
from pywinauto.application import Application as app
from pywinauto import clipboard
from pywinauto import keyboard
import time

path = "C:\\Program Files (x86)\\Kakao\\KakaoTalk\\KakaoTalk.exe"
tgtwindow = "용인시 공유전동킥보드 불법주차 신고"
kwrd = "용인시"

kakao_setup = app('uia').start(path)
kakao = app('uia').connect(path=path)

# kakao.wait(5)
# kakao.print_control_identifiers()
# kakao_dlg = kakao['카카오톡Dialog']
# kakao_dlg.print_control_identifiers()
# kakao['카카오톡']['OnlineMainView_0x00060542'].print_control_identifiers()
#
# chat_list_pane = kakao_dlg.child_window(title="ChatRoomListView_0x000f0b1c", auto_id="1150", control_type="Pane")
# chats = chat_list_pane.children(control_type="Pane")
# for chat in chats:
#     print("chats:", chat.window_text())

procs = pywinauto.findwindows.find_elements()

for proc in procs:
    print("Current process:", proc.name)
    print(proc)
    if kwrd in proc.name:
        print(f'keword {kwrd} found')
        chat = app('win32').connect(title=proc.name)
        print("chat selected and connected")
        chat_dlg = chat[tgtwindow]
        chat_dlg.print_control_identifiers()
        # print("windows:", chat.windows())
        chat_dlg.Edit.click()
        chat_dlg.type_keys('^s')
        time.sleep(1)
        save_dlg = pywinauto.Desktop(backend="win32").window(title_re='.*다른 이름으로 저장*', found_index=0)

        # Ensure the Save dialog has focus
        save_dlg.set_focus()

        # Send Enter key to confirm the Save dialog
        save_dlg.type_keys('{ENTER}')

        procs = pywinauto.findwindows.find_elements()

        for proc in procs:
            print("Current process:", proc.name)
            print(proc)

        time.sleep(1)
        # chat_dlg.set_focus()
        keyboard.send_keys('{ENTER}')
        #FIXME: works up to this point

        # active_window_handle.type_keys('{ENTER}')

        # confirm_dlg = pywinauto.Desktop(backend="win32").window(title_re='.*대화*', found_index=0)
        # confirm_dlg.type_keys('{ENTER}')
        #
        # keyboard.send_keys('{ENTER}')
        txtcontent = clipboard.GetData()
        print(txtcontent)

        break



# print("Current process:", proc.name)
#     print(proc)
#     if kwrd in proc.name:
#         print(f'keword {kwrd} found')
#         chat = app('win32').connect(title=proc.name)
#         print("chat selected and connected")
#         chat_dlg = chat.window(title=tgtwindow)
#         chat_dlg.set_focus()
#         texttxt = chat[tgtwindow]['Edit'].window_text()
#         print("test:", texttxt)
#         # chat_dlg.print_control_identifiers()
#         # for window in chat.windows():
#         #     print(window)
#         # chat_dlg.set_focus()
#         # chat_dlg['Edit'].click()
#         # chat_dlg.type_keys('^a^c')
#         # keyboard.send_keys('^a')
#         # time.sleep(1)
#
#         selected_text = chat_dlg.window_text()
#         print("text:", selected_text)
#         # txtcontent = clipboard.GetData()
#         # print("cliptext:", txtcontent)
#         break






# #time, id(hashed), raw address in korean, street address, street address2, building
# def kakao_crawl():
#     # app = Application(backend='uia').start('KakaoTalk.exe')
#     procs = pywinauto.findwindows.find_elements()
#     for proc in procs:
#         print("Current process:", proc.name)
#         if proc.name == '카카오톡':
#             print("Target identified")
#             print(proc.process_id)
#             kakao = app().connect(path=path)
#             kakao.wait(5)
#             if kakao:
#                 kakao.print_control_identifiers()
#             break




def add_to_csv():
    pass

def add_to_spreadsheet():
    pass
