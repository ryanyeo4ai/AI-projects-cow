import time
import urllib.request as urlre
from urllib.parse import (
    urljoin
)
from threading import Thread

from module.fcmsend import *
from module.stream_webcam import WebcamVideoStream

# phonenum - '휴대폰번호's
# rumnum - '승가발생 축사 번호'
# send_fcm('01012123434', '2')
server_ip = SSNET_FILE_SERVER
url_alarm = urljoin(SSNET_ALRAM_SERVER, '/api/me/users')

def stringify(response_string):
    response = ''
    for word in response_string.split():
        new_word = word
        if word == 'true':
            new_word = '\"true\"'
        if word == 'false':
            new_word = '\"false\"'
        if word == 'none':
            new_word = '\"none\"'
        if word == 'true,':
            new_word = '\"true\",'
        if word == 'false,':
            new_word = '\"false\",'
        if word == 'none,':
            new_word = '\"none\",'
        response += (new_word + ' ')
    return response


class CowManage(object):
    def __init__(self, URL, cctv_name, phone, owner):
        self.owner = owner
        self.saveStart = False
        self.rideCount = 0
        self.frameCount = 0
        self.lastFailFrameCount = 0
        self.rideBoxes = []
        self.boxes = []
        self.predicted = []
        self.start = time.time()
        # self.cap = FileVideoStream(URL)
        # self.cap = cv2.VideoCapture(URL)

        # 내부 영상저장용 목적
        self.internal_cap = cv2.VideoCapture(URL)

#############################################################
        # 기존 스트리밍 영상을 분석 하는 기능 (URL)
        try:
            urlre.urlretrieve(URL)
            self.isRunning = True
            self.cap = WebcamVideoStream(URL)
            self.cap.start()
            # print(URL)
        except urlre.HTTPError:
            self.isRunning = False
#############################################################

#############################################################
        # 농가의 영상을 직접 분석 하도록 수정
        # self.cap = self.get_cap_instance(URL)
#############################################################

        # self.cap = M3U8Stream(URL)
        # time.sleep(1)
        self.videoName = ''
        self.saveStartFrame = 0
        self.saveVideo = False
        self.frames = []
        self.blacklistCenter = (-200, -200)
        self.whiteRatio = 0
        self.whiteRatioZero = 0
        self.cctv_name = cctv_name
        self.savedFrameNumber = 0
        self.fps = 15
        self.duration_second = 5
        self.URL = URL
        self.phone = phone
        self.try_count = 0
        self.accuracy = 0
        self.segment = None
        self.fail_count = 0

    def get_cap_instance(self, url):
        cap = cv2.VideoCapture(url)
        self.isRunning = True

        return cap

    def setReCapture(self):
        self.try_count += 1
        # print('%s / %s' % (str(self.URL), str(self.try_count)))
        if self.try_count == 1:
            if self.frameCount - self.lastFailFrameCount > 5:
                self.try_count = 0
        if self.try_count > 5:
            self.isRunning = False
        self.lastFailFrameCount = self.frameCount

        if self.try_count > 3000:
            self.try_count = 0
            try:
                print(self.URL)
                urlre.urlretrieve(self.URL)
                success = True
            except:
                success = False
                self.lastFailFrameCount = self.frameCount
                print('empty %s' % self.URL)
            if success:
                self.isRunning = True
                self.cap.restart()

                print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n\n')
                print('%s cow Reconnected' % self.URL)
                print(self.phone)
                print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n\n')
                return True, True
            else:
                return True, False
        else:
            return False, False

    def isEmpty(self):
        if len(self.frames) == 0:
            return True
        else:
            return False

    def delete(self):
        try:
            del self.frames
        except:
            print('delete problem')
        self.frames = []

    def setVideoName(self, directory, title):
        # self.videoName = '%s/%s.mp4' % (directory, title) #2022.05.21 by Ryan
        self.videoName = '%s/%s.mp4' % (directory, title)
        #print(f'[0522] setVideoName() self.videoName : {self.videoName}') #2022.05.22 by Ryan

    def addFrame(self, frame):
        self.frames.append([self.frameCount, frame])
        if len(self.frames) > 6 * 15:
            del self.frames[6 * 15:]

    def setSavedFrameNumber(self):
        self.savedFrameNumber = self.frameCount

    def checkDuration(self):
        # if self.saved
        if self.frameCount - self.savedFrameNumber > self.fps * self.duration_second:
            return True
        else:
            return False

    def saveFrame(self, frame, accuracy):
        cv2.imwrite(self.videoName[:-4] + '.jpg', frame)
        print(f'[0522] saveFrame')
        print(f'[0522] self.videoName : {self.videoName[:-4] + ".jpg"}')

        with open(self.videoName[:-4] + '_' + accuracy, 'w') as f:
            f.close()

    def checkFCMDuration(self):
        if self.frameCount - self.saveStartFrame > 15 * 60:
            return True
        else:
            return False

    def setZeros(self):
        self.saveStart = False
        self.rideCount = 0
        self.whiteRatio = 0
        self.whiteRatioZero = 0

    def countFailed(self):
        self.fail_count += 1
        return self.fail_count

    def get_size(self):
        return self.cap.size()

class StreamManager(CowManage):
    def __init__(self, URL, cctv_name, phone, owner):
        self.processing =False
        super(StreamManager, self).__init__(URL, cctv_name, phone, owner)

    def __get_movie_file_name(self):
        if self.videoName != "":
            return self.videoName
        # FIXME: return none?
        return "/data/ServerManager/data/FarmCCTV/01086212701/01086212701_20200727234240_4.mp4"

    def __get_image_file_name(self):
        filename = self.__get_movie_file_name()
        return filename[:-4] + '.jpg'

    def __rescale_size(self, width, height, percent=50):
        width = int(width * percent/ 100)
        height = int(height * percent/ 100)

        return width, height

    def __resize_frame(self, frame, width, height):
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    def __send_movie_file(self, fileDir):
        mode = 'media'
        # 05.21 by Ryan
        #print(f'[0521] __send_movie_file fileDir : {fileDir}')

        fileDir = os.path.normpath(fileDir)
        base = os.path.basename(fileDir)
        index = int(float(base.split('_')[-1][:-4])) # 2022.05.21 by Ryan
        
        phone = base.split('_')[0]
        server_folder = SSNET_FILE_FOLDER
        server_folder += '%s/%s' % (str(mode), phone) # windows10

        # 05.21 by Ryan
        # print(f'[0521] fileDir : {fileDir}')
        # print(f'[0521] server_folder : {server_folder}')
        # print(f'[0521] server_ip : {server_ip}')
        # print(f'[0521] self.videoName : {self.videoName}')
        modeDB = mode
       
        # print(f'[0521] mode : {mode}') # 05.21 by Ryan
        if mode == 'media':
            print ("이미지 파일 전송!")
            print(f'[0521] self.videoName : {self.videoName}')
            sendSCP(self.videoName, server_ip, server_folder)
            sendSCP(self.videoName[:-4] + '.jpg', server_ip, server_folder)
            modeDB = 'movies'

        uploadCowDatabase(phone, base, modeDB)

        FCMsend = getAlarmInformation(phone, mode)

        if phone in ['01087905034', '01087870803']:
            FCMsend = True
        if FCMsend:
            #index = 0
            send_fcm(phone, str(index), modeDB)

        print('%s success' % base)
        print('---------------------------------------------')

    def __create_movie_file(self, first_frame):
        # 2022.05.21 by Ryan
        # filename = self.videoName
        # self.__send_movie_file(filename)
        # return

        if self.processing:
            print ("현재 영상을 처리 중입니다.")
            return

        self.processing = True

        # 이미지 파일 전송
        image_file_name = self.__get_image_file_name()
        cv2.imwrite(image_file_name, first_frame)

        print (f'create_movie_image_file : {image_file_name}')

        frames = []
        fps = 15
        frame_count = 120

        frames.append(first_frame)

        # 원래 영상의 사이즈에서 크기를 조절
        width, height = self.get_size()
        # width, height = self.__rescale_size(width, height)
        '''
        for i in range(frame_count):
            ret, frame = self.internal_cap.read()
            frame = self.__resize_frame(frame, width, height)
            frames.append(frame)

        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        print (filename)


        for frame in frames:
            out.write(frame)
        '''
        #정지된 영상 저장
        filename = self.__get_movie_file_name()

        if not os.path.isfile(filename):
            fourcc = cv2.VideoWriter_fourcc(*'h264')
            out = cv2.VideoWriter(filename,fourcc, fps, (width, height))

            for i in range(frame_count):
                out.write(first_frame)

            out.release()
            self.__send_movie_file(filename)
        else:
            print ("파일이 존재합니다. : {}".format(filename))

        self.processing = False

    def start_save_process(self, frame=None):
        if not self.processing:
            proc = Thread(target=self.__create_movie_file, args=(frame.copy(),))
            proc.start()

class StreamManagerTest(StreamManager):
    def __init__(self, URL, cctv_name, phone, owner):
        super(StreamManagerTest, self).__init__(URL, cctv_name, phone, owner)

    # 함수를 재정의 하여 탐지 결과를 전송하지 않음
    def start_save_process(self, frame=None):
        print ("탐지 결과를 전송하지 않음")
