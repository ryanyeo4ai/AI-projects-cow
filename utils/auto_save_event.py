import sys, os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from threading import Thread
import pandas as pd
from module.lib import *
from SecureCCTV.darknet_model.yolo import YOLO


# 심응식 rtsp://admin:ssnet9000!@ses2663.iptime.org:3151/Streaming/channels/101
# 테스트 http://test.ssnetworks.kr/videos/farmcctv.m3u8

n_max_frames = 300
urls = []
directory = os.path.abspath('Manager/users_r_poly.xlsx')
UserExcel = pd.read_excel(directory, sheet_name='Sheet1')
url_list = UserExcel['IP'].tolist()
for i in url_list:
    if i[0]=='p':
        urls.append('rtsp://'+i[2:])

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

yolo = YOLO()

def save_event(url,count):
    cap.open(url)
    frames = []
    detected = False
    frames_count = 0
    while True:
        ret, frame = cap.read()
        frames_count += 1
        if ret:
            frames.append(frame)

            if not detected:
                if is_detected_secure_issue(yolo, frame):
                    detected  = True
                if len(frames) > n_max_frames:
                    del frames[0]

                continue

            # 버퍼의 3배 크기를 확보 후 저장
            if len(frames) >= (n_max_frames * 3):
                break
            if frmaes_count > 5000:
                return None
    write_frames('test'+str(count)+'.mp4', frames)
    cap.release()
    cv2.destroyAllWindows()
    print(url,'- save complet')
    return None
############################################

procs = []
count = 0
for url in urls:
    count+=1
    proc = Thread(target=save_event, args=(url,count,))
    proc.daemon = True
    procs.append(proc)
for proc in procs:
    print(url,' - start')
    proc.start()
    proc.join()
del procs


