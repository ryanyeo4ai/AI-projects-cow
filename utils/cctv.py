import pymongo

def get_db_data(phone):
    url = "mongodb://ssnetworks.kr"
    connection = pymongo.MongoClient(url, 8875)
    db = connection.stream
    cameraDB = db.camera

    result = cameraDB.find()

    names = []
    phones = []
    rtsps = []
    urls = []

    for data in result:
        if phone == data['phone']:
            m3u8_url = 'http://ssnetworks.kr:4567/live/{}/cam.m3u8'.format(str(data['_id']))
            phones.append(data['phone'])
            names.append(data['name'])
            rtsps.append('rtsp://' + str(data['cameraIp']))
            urls.append(m3u8_url)

    return urls, rtsps

phone = "01086212701"
urls, rtsps = get_db_data(phone)

for i in range(len(urls)):
    print (urls[i], rtsps[i])
