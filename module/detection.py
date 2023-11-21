
from abc import ABCMeta, abstractmethod

class Detection(metaclass = ABCMeta):
    def __init__(self):
        pass

class SecureDetection(Detection):
    def __init__(self):
        self.detected_frame = None
        super(SecureDetection, self).__init__()

    def update_detected_frame(self, frame):
        self.detected_frame = frame.copy()

    def is_detected(self):
        if self.detected_frame is not None:
            return True

        return False

    def get_detected_frame(self):
        return self.detected_frame
