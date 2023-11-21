import os,sys
import json
from pytz import timezone

from module.conf import *
import module.mysql_log

class MysqlLog(module.mysql_log.MysqlDatabase):
    def __init__(self, table):
        super().__init__(table)

    def init_cctv_event_dic(self):
        dictionary = self.init_dict()
        dictionary['event_type']=''
        dictionary['event_value']=''
        return dictionary

    def init_system_event_dic(self):
        dictionary = self.init_dict()
        dictionary['camera_type']=0
        dictionary['camera_id']=''
        dictionary['farm_id']=''
        return dictionary

    def list_to_dict_cctv_event(self, list_data):
        dictionary = self.init_cctv_event_dic()
        dictionary['container_id']=list_data[0]
        dictionary['camera_type'] = list_data[1]
        dictionary['camera_id'] = list_data[2]
        dictionary['log']=json.dumps(list_data[3])
        dictionary['farm_id'] = list_data[4]
        return dictionary

    def list_to_dict_system_event(self, list_data):
        dictionary = self.init_system_event_dic()
        dictionary['container_id']=list_data[0]
        dictionary['log']=list_data[2]
        dictionary['event_type'] = ''
        dictionary['event_value'] = '' 
        return dictionary

if __name__=="__main__":
    a = MysqlLog(CCTV_EVENT_TABLE)
    b = MysqlLog(SYSTEM_EVENT_TABLE)
    list_data = ['8ecd2fe6d0f4', 1, '0', [[[184, 431, 621, 654],[100,100,100,100]], ['car','person'], [0.8175707459449768],[0.777777777777777]],'01012341234']
    print(list_data)
    dic = a.list_to_dict_cctv_event(list_data)
    print(dic)
    a.insert_data(dic)
