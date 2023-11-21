#-*- coding: utf-8 -*-
import cv2
import pymongo


class mongo_checker():
    def __init__(self):
        url = "mongodb://ssnetworks.kr"
        self.connection = pymongo.MongoClient(url, 8875)
        self.db = self.connection.stream
        self.cameraDB = self.db.camera
        self.cap = cv2.VideoCapture()
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)
        self.fail_list = []

    def get_rtsp_list(self):
        rtsp_list = []
        name_list = []
        result = self.cameraDB.find()
        for data in result:
            rtsp_list.append(('rtsp://'+str(data["cameraIp"])))
            name_list.append((str(data['phone'])+'_'+str(data['name'])))
        return rtsp_list, name_list

    def get_cv_info(self, url, name):
        self.cap.open(url)
        filename = './tmp/'+name+'.jpg'

        if (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(filename, frame)
                print("[save] {} {}".format(name, url))
                return True

        self.fail_list.append(url)
        print("[ERROR] {} {}".format(name, url))

        return False

if __name__=="__main__":
    mongo = mongo_checker()
    rtsp_list, name_list = mongo.get_rtsp_list()
    print(len(rtsp_list))

    for i, j in zip(rtsp_list, name_list):
        for tt in range(10):
            a = mongo.get_cv_info(i, j)
            if a:
                break

    print(len(mongo.fail_list),'/',len(rtsp_list))
    print(mongo.fail_list)
