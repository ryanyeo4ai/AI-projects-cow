import sqlalchemy as db
import datetime
from pytz import timezone
from module.conf import *

class MysqlDatabase():
    def __init__(self, table):
        connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)
        self.engine = db.create_engine(connect_string)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = db.Table(table, self.metadata, autoload=True, autoload_with=self.engine)
        print(table,'-connect')
    def __del__(self):
        pass

    def insert_data(self, dic):
        query = db.insert(self.table)
        values_list = [dic]
        result_proxy = self.connection.execute(query, dic)
        result_proxy.close()

    def select_data(self):
        query = db.select([self.table])
        print(query)
        result_proxy = self.connection.execute(query)
        result_set = result_proxy.fetchall()
        print(result_set[-10::])

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

