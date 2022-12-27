from ais_gfss_parameter import using
from util.logger import log
#import redis

if using.startswith('PROD'):
    LIB_DIR = r'/home/ais_gfss/instantclient_21_4'
elif using == 'DEV_WIN_HOME':
    LIB_DIR = r'd:/install/oracle/instantclient_19_13'
else:
    LIB_DIR = r'C:\instantclient_21_3'

if using == 'PROD':
    pool_min = 40
    pool_max = 120
    pool_inc = 40
    Debug = True
else:
    pool_min = 4
    pool_max = 10
    pool_inc = 4
    Debug = True

dsn = '192.168.20.64:1521/gfss'
username = 'sswh'
password = 'sswh'
encoding = 'UTF-8'
timeout = 60       # � ��������. ����� �������, ����� �������� ������ �������������
wait_timeout = 15000  # ����� (� �������������) �������� ���������� ������ � ����, ����� ��� ��� ������ ������
max_lifetime_session = 2800  # ����� � ��������, � ������� �������� ����� ����������� �����

log.info(f"=====> DB CONFIG. using: {using}, LIB_DIR: {LIB_DIR}, DSN: {dsn}")

# if using != 'DEV_WIN_HOME':
#     db_redis = redis.from_url('redis://@10.15.15.11:6379')
#     log.info(f"=====> REDIS CREATED. using url: redis://@10.15.15.11:6379")

class SessionConfig:
    # secret_key = 'this is secret key qer:ekjf;keriutype2tO287'
    SECRET_KEY = 'this is secret key 12345 -'
    if using[0:3] == 'DEV':
        SESSION_TYPE = "filesystem"
    else:
        # SESSION_TYPE = 'redis'
        SESSION_TYPE = "filesystem"
        # SESSION_REDIS = db_redis
        SESSION_REDIS = redis.from_url('redis://@10.15.15.11:6379')
    SESSION_USE_SIGNER = True
    # SESSION_REDIS = Redis(host='10.15.15.11', port='6379')
    # SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3000
    # SQLALCHEMY_DATABASE_URI = f'oracle+cx_oracle://{username}:{password}@{dsn}'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f"----------> TYPE SESSION: {SESSION_TYPE}")