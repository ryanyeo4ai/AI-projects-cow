#-*- coding: utf-8 -*-

import sys

"""
각 서버에서 처리될 데이터의 갯수를 연산
"""
def get_page_num(total, server):
    if total % server == 0:
        return int(total / server)

    return int(total / server) + 1

"""
데이터를 나눠서 가지고옴
"""
def split_job_data(data, server_offset=0, server_count=1, server_total_count=1):
    if data == None:
        return None

    if len(data) < server_total_count:
        print ("서버의 갯수[{}]는 데이터의 갯수[{}]를 넘을 수 없습니다.".format(server_total_count, len(data)))
        sys.exit()

    page_num = get_page_num(len(data), server_total_count)
    count = page_num * server_count
    offset = server_offset * page_num

    print ("전체 {}개의 데이터 중에서 {}개를 처리합니다.".format(len(data), count))

    return data[offset:offset+count]


"""
사용 예)

result = []
total_server_count = 8

data = self.get_data()

result.extend(split_job_data(data, 0, 1, total_server_count))
result.extend(split_job_data(data, 1, 1, total_server_count))
result.extend(split_job_data(data, 2, 1, total_server_count))
result.extend(split_job_data(data, 3, 1, total_server_count))
result.extend(split_job_data(data, 4, 4, total_server_count))

직접 데이터를 서버로 나눠서 처리할 경우,
나눠진 데이터의 합이 전체 합과 일치하는지 테스트케이스로 확인하는 것을 권장

print (result)
"""
