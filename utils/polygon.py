import sys

import cv2
import numpy as np


###############################################
def poly_draw(frame, dots):
    pts = np.array (dots, np.int32)
    pts = pts.reshape ((-1,1,2))
    cv2.polylines (frame, [pts], True , (0,255,255))

###############################################

test_polygo = [[10,5], [20,30], [70,20], [50,10]]


if len(sys.argv) != 2:
    print("usage : {} RTSP URL".format(sys.argv[0]))
    sys.exit()

url = sys.argv[1]

print (url)

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

cap.open(url)

while(True):
    ret, frame = cap.read()
    poly_draw(frame, test_polygon)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

