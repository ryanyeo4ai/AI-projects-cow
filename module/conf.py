import os
# DB 접속 정보
SSNET_DB_SERVER = '127.0.0.1'
SSNET_DB_PORT = 27017

# 스트리밍 서버 정보
SSNET_STREAMING_SERVER = '192.168.0.11'
SSNET_STREAMING_PORT = '4567'

# CONF_STREAMING_SERVER_URL = 'https://beta.ssnetworks.kr/'
CONF_STREAMING_SERVER_URL = 'https://web.ssnetworks.kr/'

# 영상 및 이미지 저장 정보
SSNET_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SSNET_SAVE_DIR = SSNET_ROOT_DIR + '/data'

# 로그 저장용 mysql 정보
#db conf
#DB_HOST = '10.0.0.23'
DB_HOST = 'localhost'
DB_USER = 'ssnet'
DB_PASS = 'how-to-install-mariadb-on-ubuntu-20-04'
DB_PORT = 3306
DATABASE = 'ssnet'
CCTV_EVENT_TABLE = 'cctv_event'
SYSTEM_EVENT_TABLE = 'system_event'


SSNET_ALRAM_SERVER = 'http://localhost:8001'
SSNET_FILE_SERVER = 'ubuntu@localhost'
#SSNET_FILE_SERVER = 'ubuntu@ssnetworks.kr'
SSNET_FILE_FOLDER = '/data/www/stream/'

USER_DATA_FILE = 'Manager/users_ssnet.xlsx'
