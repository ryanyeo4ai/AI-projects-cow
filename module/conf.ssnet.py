import os
# DB 접속 정보
SSNET_DB_SERVER = '10.0.0.23'
SSNET_DB_PORT = 8875

# 스트리밍 서버 정보
SSNET_STREAMING_SERVER = '10.0.0.23'
SSNET_STREAMING_PORT = '4567'

# 영상 및 이미지 저장 정보
SSNET_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SSNET_SAVE_DIR = SSNET_ROOT_DIR + '/data'

# 로그 저장용 mysql 정보
#db conf
#DB_HOST = '10.0.0.23'
DB_HOST = 'ssnetworks.kr'
DB_USER = 'ssnet'
DB_PASS = 'ssnet369#'
DB_PORT = 3306
DATABASE = 'ssnet'
CCTV_EVENT_TABLE = 'cctv_event'
SYSTEM_EVENT_TABLE = 'system_event'


SSNET_ALRAM_SERVER = '10.0.0.23:3001'
SSNET_FILE_SERVER = 'ubuntu@10.0.0.23'
#SSNET_FILE_SERVER = 'ubuntu@ssnetworks.kr'
SSNET_FILE_FOLDER = '/data/www/stream/'

USER_DATA_FILE = 'Manager/users_ssnet.xlsx'
