import time
from datetime import datetime, timedelta
import pymongo
import sys 

class CtrlMongo():
    def __init__(self):
        url = "mongodb://ssnetworks.kr"# + SSNET_DB_SERVER
        self.connection = pymongo.MongoClient(url, 8875)
        self.db = self.connection.stream
        self.camera = self.db.camera
        self.movie = self.db.movie
        self.person = self.db.person

    def get_collection(self, collection, query={}):
        #print(query)
        result = collection.find(query)
        data = [x for x in result]
        return data

    def get_query(self, date=None):
        if not date:
            date_1 = (datetime.today()+timedelta(1)).strftime('%Y-%m-%d')
            date = datetime.today().strftime('%Y-%m-%d')
        else:
            date_1 = (datetime.strptime(date ,'%Y-%m-%d')+timedelta(1)).strftime('%Y-%m-%d')
            date = datetime.strptime(date ,'%Y-%m-%d').strftime('%Y-%m-%d')
        query = {'created' : {'$gte':date, '$lt':date_1}}#+timedelta(1)}}
        #print(query)
        return query

    def get_result(self, date=None):
        camera = self.get_collection(self.db.camera)
        movie = self.get_collection(self.db.movie, self.get_query(date))
        person = self.get_collection(self.db.person, self.get_query(date))

        tmp = []
        for i in camera:
            tmp.append(i['phone'])
        tmp = list(set(tmp)) # 카메라컬렉션을 기준으로 농가번호 확인
        tmp2 = []
        for i in range(len(tmp)):
            for j in camera:
                if tmp[i]==j['phone']:
                    tmp2.append({'phone':tmp[i], 'name':j['name'],'cow_count':0, 'person_count':0})
                    break
        #print('카메라컬렉션 기준 농가')
        #print(tmp)
        #print(tmp2)
        for i in movie:
            for j in tmp2:
                if i['phone'] in j['phone']:
                    j['cow_count']+=1
        for i in person:
            for j in tmp2:
                if i['phone'] in j['phone']:
                    j['person_count']+=1
        for i in tmp2:
            print(i)

        '''
    def get_result(self, date=None):
        camera = self.get_collection(self.db.camera)
        movie = self.get_collection(self.db.movie, a.get_query(date))
        person = self.get_collection(self.db.person, a.get_query(date))

        tmp = []
        for i in camera:
            tmp.append(i['phone'])
        tmp = list(set(tmp)) # 카메라컬렉션을 기준으로 농가번호 확인
        tmp2 = tmp.copy()
        for i in range(len(tmp2)):
            for j in camera:
                if tmp2[i]==j['phone']:
                   tmp2[i]=j['name']
                    break
        #print('카메라컬렉션 기준 농가')
        #print(tmp)
        movie_result = dict.fromkeys(tmp, 0)
        for i in movie:
            if i['phone'] in tmp:
                movie_result[i['phone']]+=1
        #print(movie_result)
        movie_result_name={}
        for key, b in zip(movie_result.items(), tmp2):
            movie_result_name[b]=key[1]

        person_result = dict.fromkeys(tmp, 0)
        for i in person:
            if i['phone'] in tmp:
                person_result[i['phone']]+=1
        #print(person_result)
        person_result_name={}
        for key, b in zip(person_result.items(), tmp2):
            person_result_name[b]=key[1]

        print('{} 승가'.format(date))
        #print(movie_result_name)
        for value, key in enumerate(movie_result_name):
            print(key, value)
        print('\n{} 출입'.format(date))
        for value, key in enumerate(person_result_name):
            print(key, value)
        #print(person_result_name)
        '''
if __name__ == '__main__':
    #a.get_result()

    if len(sys.argv) != 2:
        print ("{} [YYYY-MM-DD]".format(sys.argv[0]))
        sys.exit()

    b = CtrlMongo()
    b.get_result(sys.argv[1])
    # a.get_result('2022-01-10') #없으면 오늘
