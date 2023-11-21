import cv2
import sys
import time
import numpy as np

class Polygon():
    def __init__(self):
        pass

    def xywh(self, x, y, w, h):
        x = x+w/2
        y = y+h/2
        return x, y

    def point_inside_polygon(self, x ,y ,poly):
        n = len(poly)
        inside =False
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside

    def poly_draw(self,frame, dots, point_x, point_y):
        pts = np.array (dots, np.int32)
        pts = pts.reshape ((-1,1,2))
        cv2.polylines (frame, [pts], True , (0,255,255)) #다각형 그리기
        cv2.circle(frame, (int(point_x), int(point_y)), 8, (100, 100, 255), -1) #point 그리기
        return self.point_inside_polygon(point_x, point_y ,dots)


