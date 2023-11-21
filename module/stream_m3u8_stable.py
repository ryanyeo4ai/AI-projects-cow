import numpy
import pymongo
import m3u8
import subprocess
from threading import Thread
import cv2
import time
import datetime

class M3U8Stream:
    def __init__(self, src=0, name="farmName"):
        self.src = src

        self.setCapture()
        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        # self.frame = None
        self.stopped = False
        self.ret = True
        self.failCount = 0

    def setCapture(self):
        self.pipe = subprocess.Popen(["ffmpeg", "-i", self.src,
                                      "-loglevel", "quiet",  # no text output
                                      # "-an",  # disable audio
                                      "-f", "image2pipe",
                                      "-pix_fmt", "bgr24",
                                      # "-r", "20",
                                      "-vcodec", "rawvideo", "-"],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        time.sleep(0.2)
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            try:
                raw_image = self.pipe.stdout.read(1920 * 1080 * 3)
                self.frame = numpy.fromstring(raw_image, dtype='uint8').reshape((1080, 1920, 3))
                time.sleep(1/20)
            except:
                self.ret = False
                if self.failCount == 0:
                    print(datetime.datetime.now())
                    print(str(self.src) + ' failed')
                self.failCount += 1

            if self.failCount > 15 * 30:
                self.failCount = 0
                self.setCapture()
                self.start()
                print('reconnected')

    def read(self):
        # return the frame most recently read
        return self.ret, self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def destroy(self):
        pass