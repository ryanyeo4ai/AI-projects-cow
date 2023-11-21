import numpy
import pymongo
import m3u8
import subprocess
from threading import Thread, Timer
from multiprocessing import Process
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
        self.pipe = subprocess.Popen(["ffmpeg", "-re", "-i", self.src,
                                      "-loglevel", "quiet",  # no text output
                                      # "-an",  # disable audio
                                      "-f", "image2pipe",
                                      "-pix_fmt", "bgr24",
                                      # "-r", "15",
                                      "-avoid_negative_ts", "make_zero",
                                      "-vsync", "1",
                                      "-async", "1",
                                      "-acodec", "copy",
                                      # "-vcodec", "copy",
                                      # "-f", "hls",
                                      "-segment_list_size", "2",
                                      "-hls_time", "1",
                                      "-hls_flags", "delete_segments",
                                      "-vcodec", "rawvideo", "-"
                                      ],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # def setCapture(self):
    #     self.pipe = subprocess.Popen(["ffmpeg", "-re", "-i", self.src,
    #                                   "-loglevel", "quiet",  # no text output
    #                                   # "-an",  # disable audio
    #                                   "-f", "image2pipe",
    #                                   "-pix_fmt", "bgr24",
    #                                   "-r", "15",
    #                                   "-vcodec", "rawvideo", "-"],
    #                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

        # self.update()

    def update(self):
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            try:
                raw_image = self.pipe.stdout.read(1920 * 1080 * 3)
                self.frame = numpy.fromstring(raw_image, dtype='uint8').reshape((1080, 1920, 3))
                self.ret = True
            except:
                self.ret = False
                self.frame = None
            # time.sleep(1/20)
            time.sleep(0.068)

    def read(self):
        # return the frame most recently read
        return self.ret, self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def destroy(self):
        # indicate that the thread should be stopped
        self.stopped = True
        try:
            self.pipe.kill()
        except:
            print('success to kill')
            pass

    def restart(self):
        self.destroy()
        self.stopped = False
        self.setCapture()
        self.start()
