import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from module.stream_webcam import WebcamVideoStream

from module.cctv import CCTV
from module.conf import *

"""
offset, weight, count 등을 입력하였을 때, 분석할 수 있는 CCTV 목록 확인
"""
class CheckCCTV(CCTV):
    def __init__(self, type_str, server_offset=0, server_count=1, server_total_count=1):
        super(CheckCCTV, self).__init__(type_str, server_offset, server_count, server_total_count)

    def get_m3u8_url(self, key):
        pass

cctv = CheckCCTV("c", 4, 1, 5)

for url in cctv.URLs:
    print (url)
