import cv2
import sys
import time
import numpy as np


###############################################
def contour_draw(frame): #이전영상이 존재해야하므로 if ret: 부분 필수
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(frame_gray, 127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
    point = (15,15) #test point
    for cnt in contours:
        cv2.drawContours(frame, [cnt], 0, (255, 0, 0), 2)
        a = cv2.pointPolygonTest(cnt, point, False) # -1, 1, 0 == out, in, on
        if a>=1:
            cv2.circle(frame, point, 8, (100, 100, 255), -1)
###############################################


if len(sys.argv) != 2:
    print("usage : {} RTSP URL".format(sys.argv[0]))
    sys.exit()

url = sys.argv[1]

print (url)

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

cap.open(url)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        contour_draw(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

