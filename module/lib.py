import cv2

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from FarmCCTV.darknet_model.yolo import YOLO

def write_frames(filename, frames):
    # 아래의 인코딩 방식은 docker 안에서 실행해야 함.
    writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 15, (1920, 1080))

    for frame in frames:
        writer.write(frame)

    writer.release()

def is_detected_secure_issue(yolo, frame):
    boxes, predicted, accuracies = yolo.detect_image(frame, "")

    if len(boxes) > 0:
        print (boxes, predicted, accuracies)
        return True

    return False
