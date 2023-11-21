import shutil
import subprocess
import os
from urllib.parse import urljoin

import cv2
import requests
from pyfcm import FCMNotification
import time

from module.conf import *
from module.s3_api import *

# phonenum - '휴대폰번호'
# rumnum - '승가발생 축사 번호'
# send_fcm('01012123434', '2')
server_ip = SSNET_FILE_SERVER
url_alarm = urljoin(SSNET_ALRAM_SERVER, '/api/me/users')

def send_fcm(phonenum, camnum, mode):
    # 앱 토큰 가져오기
    url = urljoin(SSNET_ALRAM_SERVER, '/api/find/appTokens')
    data = {'phone': phonenum}
    # print(data)
    response = requests.post(url, headers={'Authorization': 'cc090ddf71d2866a77af6280'}, data=data)
    size = len(response.json())
    appToken = []
    for i in response.json():
        appToken.append(i['appToken'])

    # 파이어페이스 키
    push_service = FCMNotification(api_key="AAAAEA6TC-4:APA91bHutD9MS1Pj5KRftuqRP8u29lMTds2c64FMQE2sdeoRZRKNyw8i3JNQ5bJJ5DQVpQGMwMv9tNIRrHqz_nsFGtZNTm51N2UfB8GZyF0cq1tnH4oVKRpkre03swiS2lTJCUvgweCw")

    # fcm 메세지
    message_title = ""
    message_body = camnum + ""
    clickAction = ""
    if mode == 'movies':
        message_title = "승가 발생"
        message_body = camnum + "번 축사에서 승가가 발생했습니다."
        clickAction = "VideolistActivity"
    elif mode == 'person':
        message_title = "출입 확인"
        message_body = camnum + "번 카메라에서 출입자가 발생했습니다."
        clickAction = "PeopleActivity"
    elif mode == 'car':
        message_title = "차량 확인"
        message_body = camnum + "번 카메라에서 출입차량이 발생했습니다."
        clickAction = "CarActivity"
    elif mode == 'check':
        message_title = "ride"
        message_body = camnum
        clickAction = "VideolistActivity"
    data_message = {
        "title": message_title,
        "content": message_body,
        "clickAction": clickAction
    }

    result = push_service.notify_multiple_devices(registration_ids=appToken, data_message=data_message)
    print(result)


# mode = {'movies', 'car', 'person'}
def uploadCowDatabase(myphone, file_name, mode):
    print(f'[1106] phone : {myphone}')
    print(f'[1106] file_name : {file_name}')
    print(f'[1106] mode : {mode}')

    timezone = str(int(time.localtime().tm_gmtoff / 60 / 60)).rjust(2, '0')

    if mode == 'movies':
        url = urljoin(SSNET_ALRAM_SERVER, f'/api/me/{str(mode)}')
    elif mode == 'person':
        url = urljoin(SSNET_ALRAM_SERVER, f'/api/create/{str(mode)}')
    else:
        url = urljoin(SSNET_ALRAM_SERVER, f'/api/create/{str(mode)}')

    # print(f'[05/26] url : {url}')
    response = requests.post(url, headers={'Authorization': 'cc090ddf71d2866a77af6280'},
                             data={'phone': myphone, 'name': file_name})
    print(response.json())
    api = ServerAPI(
        # base_url='http://localhost:3000/serverapi',
    )
    server_folder = SSNET_FILE_FOLDER + 'media/'
    upload_file_name = file_name[:-4] + '.jpg'
    upload_dir_name = file_name.split('_')[0]
    server_folder += upload_dir_name + '/'
    my_camera_name = file_name[:-4].split('_')[2]
    created_date = file_name[:-4].split('_')[1] #2022 1114 07 18 36
    created_year = created_date[:4] #2022
    created_month = created_date[4:6] #11
    created_day = created_date[6:8] #14
    created_hour = created_date[8:10] #07
    created_min = created_date[10:12] #18
    created_sec = created_date[12:14] #36

    result = api.upload_cow_mount(
        file_path=server_folder + upload_file_name,
        camera_name=my_camera_name,
        #created_at=None,
#	    created_at=f'{created_year}-{created_month}-{created_day} {created_hour}:{created_min}:{created_sec}+{timezone}:00',
        # created_at=created_year + '-' + created_month + '-' + created_day + '-' + created_hour + '-' + created_min + '-' + created_sec,
        phone=myphone,
    )
    print()
    print(result)
    print(f'[1106] file_path : {server_folder + upload_file_name}')
    print(f'[1106] camera_name : {my_camera_name}')
    print(f'[1106] created_at : {created_date}')
    print(f'[1106] phone : {myphone}')

    print()

def getAlarmInformation(phone, mode):
    FCMsend = False
    response = requests.get(url_alarm,
                             headers={'Authorization': 'cc090ddf71d2866a77af6280'})
    data = response.json()
    try:
        for d in data:
            if d['phone'] == phone:
                alarm = [d['isPersonAlarm'], d['isCowAlarm']]
                print('phone: %s, person: %s, cow: %s' % (phone, alarm[0], alarm[1]))
                if mode == 'media':
                    if alarm[1] is True:
                        FCMsend = True
                        print('send True')
                else:
                    if alarm[0] is True:
                        FCMsend = True

                return FCMsend
    except:
        print('phone: %s -> something wrong while checking alarm' % (phone))
        return False


# mode = {'media', 'car', 'person'}
def sendFile(fileDir, FCMsend, saveFrame, mode):
    test = False
    print(f"sendFile({fileDir},{FCMsend},{saveFrame},{mode})")
    fileDir = os.path.normpath(fileDir)
    base = os.path.basename(fileDir)
    index = int(float(base.split('_')[-1][:-4]))
    phone = base.split('_')[0]
    server_folder = SSNET_FILE_FOLDER
    server_folder += '%s/%s' % (str(mode), phone) # windows10
    error = False
    if mode == 'media':
        print('image to video')
        error = imageToVideo(fileDir, saveFrame)
    else:
        error = False

    if test is False:
        if error is False:
            sendSCP(fileDir, server_ip, server_folder)

            modeDB = mode
            if mode == 'media':
                sendSCP(fileDir[:-4] + '.jpg', server_ip, server_folder)
                modeDB = 'movies'

            uploadCowDatabase(phone, base, modeDB)

            FCMsend = getAlarmInformation(phone, mode)

            if phone in ['01087905034', '01087870803']:
                FCMsend = True
            if FCMsend:
                send_fcm(phone, str(index), modeDB)
                # send_fcm('01012123434', str(index), modeDB)
                # if modeDB == 'movies':
            # send_fcm('01012123434', '%s %s' % (str(phone), str(index)), 'check')
            # os.remove(fileDir)
            print('%s success' % base)
            print('---------------------------------------------')
        else:
            print('save error')


def sendSCP(fileDir, server_ip, server_folder):
    print(f'sendSCP({fileDir}, {server_ip}, {server_folder})')
    print(f'[1106] fileDir : {fileDir}')
    print(f'[1106] server_folder : {server_folder}')
    # send = subprocess.Popen("scp -r %s %s:%s" % (fileDir, server_ip, server_folder), shell=True,
                            # stdin=subprocess.PIPE)
    try:
        if not os.path.exists(server_folder):
            os.makedirs(server_folder)
    except OSError:
        print(f'Failed to create {server_folder} ')

    cp_command = "cp %s %s/."%(fileDir, server_folder)
    print(f'cp command : {cp_command}')
    os.system(cp_command)
    # scp -r /tmp/hello.txt ubut10.0.0.23:/data/
    dirName = os.path.dirname(fileDir)
    base = os.path.basename(fileDir)

def imageToVideo__ffmpeg(videoDir, saveFrame):
    file = videoDir[:-4] + '.avi'
    writer = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*'MJPG'), 4, (640, 360))
    # writer = cv2.VideoWriter(videoDir, cv2.VideoWriter_fourcc(*'h264'), 30, (640, 360))

    for frame in saveFrame:
        writer.write(frame[1])

    writer.release()
    cmd = 'ffmpeg -i ' + file + ' -c:v libx264 ' + videoDir
    send = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
    out, error = send.communicate(input=None, timeout=None)
    os.remove(file)
    print('save success')


def imageToVideo(videoDir, saveFrame):
    try:
        h, w = saveFrame[0][1].shape[:2]
        writer = cv2.VideoWriter(videoDir, cv2.VideoWriter_fourcc(*'h264'), 4, (int(w), int(h)))

        for frame in saveFrame[:4 * 8]:
            writer.write(frame[1])

        writer.release()
        print('save success')
        return False
    except:
        print('save failed')
        return True


