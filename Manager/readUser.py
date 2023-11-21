import pandas as pd
import pymongo
from module.conf import *

def readusers():
    farms = []
    IPs = []
    phones = []
    real_phones = []

    url = "mongodb://" + SSNET_DB_SERVER

    connection = pymongo.MongoClient(url, SSNET_DB_PORT)
    db = connection.stream
    cameraDB = db.camera

    result = cameraDB.find()
    for data in result:
        phones.append(data['phone'])
        IPs.append(str(data['cameraIp']))
        # print(str(data['cameraIp']))
    return phones, IPs

# def readusers(file='Manager/users_r_poly.xlsx'):
def readusers_prev(file=USER_DATA_FILE):
    directory = os.path.abspath(file)
    UserExcel = pd.read_excel(directory, sheet_name='Sheet1')
    farm_list = UserExcel['Name'].tolist()
    Phone_list = UserExcel['Phone'].tolist()
    IP_list = UserExcel['IP'].tolist()
    #Line_list = UserExcel['Line'].tolist()
    Line_list = UserExcel['polygon'].tolist()
    farms = []
    phones = []
    real_phones = []
    lines = []
    secures_ip = []

    for i, farm in enumerate(farm_list):
        if str(farm) != 'nan':
            farms.append(str(farm))
        else:
            farms.append(farms[-1])

    for i, phone in enumerate(Phone_list):
        if str(phone) != 'nan':
            phones.append('0' + str(int(float(phone))))
            real_phones.append('0' + str(int(float(phone))))
        else:
            # phones.append(phones[-1])
            real_phones.append(phones[-1])

    for i, line in enumerate(Line_list):
        if str(line) != 'nan' and str(line) != '--':
            #temp = line.split(',')
            #lines.append([temp[0], temp[1],
            #              (int(float(temp[2])), int(float(temp[3]))),
            #              (int(float(temp[4])), int(float(temp[5])))])
            lines.append(list(eval(line)))
        else:
            lines.append([])

    f_list = list(dict.fromkeys(farms))
    IPs = [[] for _ in range(len(f_list))]
    # LINEs = [[] for _ in range(len(f_list))]
    LINEs = []

    for i, ip in enumerate(IP_list):
        IPs[f_list.index(farms[i])].append(ip)
        if lines[i] != []:
            LINEs.append(lines[i])
            secures_ip.append(real_phones[i])

    #poly_list = UserExcel['polygon'].tolist()
    #polys = []
    #for i, poly in enumerate(poly_list):
    #    if str(poly) != 'nan' and str(poly) != '--':
    #        polys.append(list(eval(poly)))
    #    else:
    #        polys.append([])
    #for i in polys:
    #    if len(i)>0:
    #        print(i[0],i[1])
    return f_list, phones, LINEs, IPs, real_phones, farms, secures_ip
