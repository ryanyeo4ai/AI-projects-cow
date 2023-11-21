import cv2
import sys

if len(sys.argv) != 3:
    print("usage : {} [RTSP URL] [filename]".format(sys.argv[0]))
    sys.exit()

url = sys.argv[1]

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)
cap.open(url)

# 아래의 인코딩 방식은 docker 안에서 실행해야 함.
writer = cv2.VideoWriter(sys.argv[2], cv2.VideoWriter_fourcc(*'MJPG'), 5, (1920, 1080))

while True:
    try:
        ret, frame = cap.read()

        if ret:
            writer.write(frame)

    except:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()

