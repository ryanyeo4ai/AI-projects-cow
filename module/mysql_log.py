import sqlalchemy as db
import datetime
from pytz import timezone
from module.conf import *

class MysqlDatabase():
    def __init__(self, table):
        pass
    def __del__(self):
        pass

    def insert_data(self, dic):
        pass

    def select_data(self):
        return []

    def get_dict_sql(self, dictionary):
        now = datetime.datetime.now()
        table='test_tcp'
        columns_string= "("+"\,".join(dictionary.keys())+")"
        values_string = "("+"\,".join(map(str, dictionary.values()))+")"
        sql = """INSERT INTO %s %s VALUES %s"""%(table, columns_string, values_string)
        return sql

    def init_dict(self):
        dictionary = {
                'time': datetime.datetime.now(timezone('Asia/Seoul')),
                'log' : '',
                'container_id' : ''
                }
        return dictionary

