#-*- coding: utf-8 -*-
import pymongo

class mongo_checker():
    def __init__(self, date):
        url = "mongodb://ssnetworks.kr"
        self.connection = pymongo.MongoClient(url, 8875)
        self.db = self.connection.stream
        self.personDB = self.db.person
        self.date = date
        self.get_person_container(self.date)

    def get_person_container(self, date):
        self.person_container = []
        result = self.personDB.find()
        for data in result:
            if int(data['name'][12:20]) >= int(date) and str(data['name'][:11]) != '01012345678': #'20200609':
                self.person_container.append(data['name'])

    def get_farm(self):
        farm = []
        for data in self.person_container:
            if data[:11] not in farm:
                farm.append(data[:11])

        for i in range(len(farm)):
            count = 0
            for data in self.person_container:
                if data[:11] == farm[i]:
                    count+=1
            farm[i] = {farm[i]:count}

        return farm

    def find_person(self):
        farm = self.get_farm()
        print(self.date,'이후 모든 이미지수',len(self.person_container))
        print('총농장 38개중 secu농장 29개')
        print('secu농장 총 29개 중 기간 중 탐지농가 총 ', len(farm), '개')
        print(farm)

    def get_farmimage_files(self, farm_phone):
        files_list = []
        for data in self.person_container:
            if data[:11] == farm_phone:
                files_list.append(data) 

        return files_list

if __name__=="__main__":
    ##test##
    mongo = mongo_checker('20200610')
    farm = mongo.find_person()
    print(farm)
    files_list = mongo.get_farmimage_files('01044560793')
    print(files_list)
