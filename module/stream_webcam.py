# import the necessary packages
import gc
import time
from threading import Thread

import cv2


# from memory_profiler import profile


class WebcamVideoStream(object):
    def __init__(self, src=0, name="WebcamVideoStream"):
        self.src = src
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        # time.sleep(2)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.try_count = 0
        self.prior_frame = None

    def start(self):
        pass
#        # start the thread to read frames from the video stream
#        t = Thread(target=self.update, name=self.name, args=())
#        # t = Timer(1/15, self.update)
#        t.daemon = True
#        t.start()
#        time.sleep(0.2)
#        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            try:
                (self.grabbed, self.frame) = self.stream.read()
            except:
                print('except in update')
                self.grabbed = False
                self.frame = None

            time.sleep(0.068)

    def read(self):
        return self.stream.read()
        # return the frame most recently read
        return self.grabbed, self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def destroy(self):
        self.stream.release()

    def restart(self):
        self.stop()
        try:
           print(1)
           gc.collect()
        except:
            print('destroy')
        try:
            print(2)
            self.stream = cv2.VideoCapture(self.src)
        except:
            print('set stream')
        try:
            print(3)
            (self.grabbed, self.frame) = self.stream.read()
        except:
            print('read stream')
        self.stopped = False
        try:
            print(4)
            self.start()
        except:
            print('start failed')
        print('success to restart')
        time.sleep(0.2)

    def size(self):
        return int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

class WebcamVideoStreamThread(WebcamVideoStream):
    def __init__(self, src=0, name="WebcamVideoStream"):
        super(WebcamVideoStreamThread, self).__init__(src, name)

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        # t = Timer(1/15, self.update)
        t.daemon = True
        t.start()
        time.sleep(0.2)
        return self

    def read(self):
        # return the frame most recently read
        return self.grabbed, self.frame
