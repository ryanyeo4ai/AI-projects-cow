import cv2
import sys
import time
import json
import numpy as np

# ex) python3 draw_poly.py 1.png [[10,5],[20,30],[70,20],[50,10]]
if len(sys.argv) != 3:
    print("usage : {} [file name] [poly]".format(sys.argv[0]))
    sys.exit()

filename = sys.argv[1]
contents = sys.argv[2]

contents = contents.replace("(", "[")
contents = contents.replace(")", "]")

poly = json.loads(contents)

img = cv2.imread(filename, cv2.IMREAD_COLOR)

for dot in poly:
    img = cv2.circle(img, (dot[0], dot[1]), 5, color=(0, 0, 255), thickness=-1)

pts = np.array(poly, np.int32)

pts = pts.reshape((-1, 1, 2))
img = cv2.polylines(img, [pts], True, (0,255,255))

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

values = []

for dot in poly:
    values.append("("+str(dot[0])+","+str(dot[1])+")")

print (",".join(values))
