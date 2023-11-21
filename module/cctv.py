#-*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

import pymongo

import module.mysql
from module.conf import *
from module.job import split_job_data
from module.readExcel import checkExcel


class CCTV(metaclass = ABCMeta):
    def __init__(self, typestr, server_offset, server_count, server_total_count):
        URLs, line = self.get_excel_data(typestr, server_offset, server_count, server_total_count)

        # self.line = line
        self.URLs = self.IP = URLs
        self.IP_n = len(self.IP)
        self.cctv_event_logger = module.mysql.MysqlLog(CCTV_EVENT_TABLE)
        self.system_event_logger = module.mysql.MysqlLog(SYSTEM_EVENT_TABLE)
        self.log = []
        self.log.append(os.uname()[1])

    def __del__(self):
        dic = {} #self.system_event_logger.init_dict()
        # dic['container_id']=self.log[0]
        # dic['log'] = 'shutdown'
        # dic['event_tpye'] = 'system'
        # dic['event_value'] = '002'
        # self.system_event_logger.insert_data(dic)

    def get_excel_data(self, typestr, server_offset, server_count, server_total_count):
        URLs, line = checkExcel(typestr)

        URLs = split_job_data(URLs, server_offset, server_count, server_total_count)
        # line = split_job_data(line, server_offset, server_count, server_total_count)
        line = []
        return URLs, line

    def get_cctv_url_prefix(self):
        return 'rtsp://'

    def setM3U8(self):
        self.m3u8 = []
        self.dbRTSP = []
        self.names = []
        self.phones = []
        url = "mongodb://" + SSNET_DB_SERVER

        connection = pymongo.MongoClient(url, SSNET_DB_PORT)
        db = connection.stream
        cameraDB = db.camera

        cctv_prefix = self.get_cctv_url_prefix()

        result = cameraDB.find()
        for data in result:
            self.names.append(data['name'])
            self.phones.append(data['phone'])
            self.dbRTSP.append(cctv_prefix + str(data['cameraIp']))
            self.m3u8.append(str(data['_id']))

    @abstractmethod
    def get_m3u8_url(self, key):
        pass
