import cv2
import numpy as np
from skimage.metrics import structural_similarity

# poly 좌표로 부터 사각형 좌표를 가져옴
def get_rectangle(poly):
    xmin, ymin, xmax, ymax= get_rectangle_xyxh(poly)
    return [(xmin, ymin), (xmin + (xmax-xmin), ymin + (ymax-ymin))]


def get_rectangle_xyxh(poly):
    xmin = xmax = ymin = ymax = 0

    for xy in poly:
        if xmax == 0 or xmax < xy[0]:
            xmax = xy[0]
        if xmin == 0 or xmin > xy[0]:
            xmin = xy[0]

        if ymax == 0 or ymax < xy[1]:
            ymax = xy[1]

        if ymin == 0 or ymin > xy[1]:
            ymin = xy[1]

    return xmin, ymin, xmax, ymax

def get_similarity_score(a, b, poly):
    rect = get_rectangle(poly)

    xmin, ymin, xmax, ymax= get_rectangle_xyxh(poly)

    a_frame = a
    b_frame = b

    a_frame = a[ymin:ymax, xmin:xmax].copy()
    b_frame = b[ymin:ymax, xmin:xmax].copy()

    cv2.imwrite('/tmp/a.jpg', a_frame)
    cv2.imwrite('/tmp/b.jpg', b_frame)

    score = structural_similarity(a_frame, b_frame, channel_axis=-1)

    print(rect)
    print(score)

    return score

def draw_line(img, poly):

    pts = np.array(poly, np.int32)

    pts = pts.reshape((-1, 1, 2))
    img = cv2.polylines(img, [pts], True, (0,255,255))

    for dot in poly:
        img = cv2.circle(img, (dot[0], dot[1]), 5, color=(0, 0, 255), thickness=-1)

    rect = get_rectangle(poly)
    img = cv2.rectangle(img, rect[0], rect[1], (0,255,0), 3)

    return img

a = 'a.jpg'
b = 'b.jpg'

a_frame = cv2.imread(a)
b_frame = cv2.imread(b)

poly = [(680,230),(580,420),(1190,395),(1035,245)]


score = get_similarity_score(a_frame, b_frame, poly)
print (score)

