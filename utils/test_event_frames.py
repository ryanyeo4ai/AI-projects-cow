import cv2
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from module.lib import *
from SecureCCTV.darknet_model.yolo import YOLO

if len(sys.argv) != 2:
    print("usage : {} [filename]".format(sys.argv[0]))
    sys.exit()

filename = sys.argv[1]

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

cap.open(filename)

frames = []
yolo = YOLO()

detected = False

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        if is_detected_secure_issue(yolo, frame):
            print ("success")

cap.release()
cv2.destroyAllWindows()
