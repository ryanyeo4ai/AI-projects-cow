import cv2
import sys
import time

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
        cv2.imshow('frame', frame)
        time.sleep(1/15)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


