import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from module.lib import *
from SecureCCTV.darknet_model.yolo import YOLO


# 심응식 rtsp://admin:ssnet9000!@ses2663.iptime.org:3151/Streaming/channels/101
# 테스트 http://test.ssnetworks.kr/videos/farmcctv.m3u8

if len(sys.argv) != 3:
    print("usage : {} [RTSP URL] [filename]".format(sys.argv[0]))
    sys.exit()

n_max_frames = 150

url = sys.argv[1]
filename = sys.argv[2]

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

cap.open(url)

frames = []

yolo = YOLO()

detected = False

while True:
    ret, frame = cap.read()
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

write_frames(filename, frames)

print ("")
print ("성공적으로 저장되었습니다.")

cap.release()
cv2.destroyAllWindows()
