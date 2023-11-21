from Manager.readUser import readusers
from Manager.URLs import checkAllCCTVs


def checkExcel(mode):
    # f_list, phones, LINEs, IPs, real_phones, farms, secures_ip = readusers()

    phones, IPs = readusers()
    print(f'phones :{len(phones)}')
    print(f'IPs :{len(IPs)}')
    print(IPs)
    _, URLs, phoneAll, cctv_n = checkAllCCTVs(IPs, phones, mode)
    print(f'URLs :{len(URLs)}')
    print(URLs)
    return URLs, None
