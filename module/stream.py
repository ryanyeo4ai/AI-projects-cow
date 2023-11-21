# import the necessary packages
import time
from queue import Queue
from threading import Thread

import cv2


class FileVideoStream:
    def __init__(self, path, transform=None, queueSize=3):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.transform = transform

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queueSize)

    def getFPS(self):
        return self.stream.get(cv2.CAP_PROP_FPS)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        # t = Timer(1/15, self.update)
        t.daemon = True
        t.start()
        # time.sleep(0.4)
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                # try:
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return

                if self.transform:
                    frame = self.transform(frame)

                # add the frame to the queue
                self.Q.put(frame)
                # except:
                #     print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                #     print('fail to get frame in .read')
                #     print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                #     self.stop()
                #     self.Q.empty()
            else:
                time.sleep(2/15)  # Rest for 10ms, we have a full queue
            time.sleep(0.068)

    def read(self):
        # return next frame in the queue
        return True, self.Q.get()

    # Insufficient to have consumer use while(more()) which does
    # not take into account if the producer has reached end of
    # file stream.
    def running(self):
        return self.more() or not self.stopped

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def destroy(self):
        self.Q.empty()
        try:
            self.stream.release()
        except:
            print('fail to release stream')

