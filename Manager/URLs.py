import cv2

def checkStreaming(URL):
    cap = cv2.VideoCapture(URL)
    ret, _ = cap.read()

def checkAllCCTVs(IPs, phones, type):
    URLs = []
    phoneAll = []
    cctv_n = {}
    # for i, IP in enumerate(IPs):
    #     for ip in IP:
    #         temp_ip = ip.split('.')
    #         if temp_ip[0] == type[0]:
    #             URLs.append("rtsp://%s" % ip[2:])
    #             phoneAll.append(phones[i])
    for i, IP in enumerate(IPs):
        URLs.append(f'rtsp://{IP}')
        phoneAll.append(phones[i])
        
    print(URLs)
    elements = set(phoneAll)
    for i in range(len(elements)):
        element = list(elements)[i]
        cctv_n.update({element: phoneAll.count(element)})

    # print(len(URLs))
    # import sys
    # sys.exit()

    return '', URLs, phoneAll, cctv_n


def checkCCTVs(IPs, phones, type):
    # print('check CCTV')
    # print(IPs)
    id = 'admin'

    errored = []
    URLs = []
    for i, IP in enumerate(IPs):
        temp_ip = IP.split('.')
        # print(temp_ip)
        if temp_ip[0] == type[0] or type == 'all':
            if temp_ip[1] == 'ssnet4':
                password = 'qwerty1.'
                URL = 'rtsp://%s:%s@%s/trackID=3' % (id, password, IP[2:])
                try:
                    cap = cv2.VideoCapture(URL)
                    ret, _ = cap.read()
                    URLs.append(URL)
                    # print('%s camera' % URL)
                except:
                    errored.append(str(IP[2:]))
            elif temp_ip[1] in ['snsway1', 'snsway2']:
                password = 'qawsedrftg1'
                URL = 'rtsp://%s:%s@%s/profile3/media.smp' % (id, password, IP[2:])
                try:
                    cap = cv2.VideoCapture(URL)
                    ret, _ = cap.read()
                    URLs.append(URL)
                    # print('%s camera' % URL)
                except:
                    errored.append(str(IP[2:]))
            else:
                # print('new %s' % str(IP[2:]))
                URLs.append(IP[2:])

    errorMessage = ''
    for error in errored:
        errorMessage = errorMessage + error

    return errorMessage, URLs

