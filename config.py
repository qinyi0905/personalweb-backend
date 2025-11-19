import os
from datetime import timedelta

SECRET_KEY = "a8oUJbhGEErf"

# 项目所在根路径
BASE_DIR = os.path.dirname(__file__)

DB_USERNAME = os.getenv('DB_USERNAME', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'RMA3_atm2')
DB_HOST = os.getenv('DB_HOST', '172.29.174.90')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'personalweb')

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CACHE_TYPE = "RedisCache"
CACHE_DEFAULT_TIMEOUT = 300
CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', '172.29.174.90')
CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT', '6379')
CACHE_REDIS_PASSWORD = os.getenv('CACHE_REDIS_PASSWORD', "7upJvu2eTuRg")

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

BANNER_IMAGE_SAVE_PATH = os.path.join(BASE_DIR, "media", "banner")
TOOL_ICON_SAVE_PATH = os.path.join(BASE_DIR, "media", "tool", "icon")

PER_PAGE_COUNT=10


NGINX_ACCESS_LOG_PATH = "/var/log/personalweb/gunicorn_access.log"
#NGINX_ACCESS_LOG_PATH = "C:\\Users\\admin\\Downloads\\access.log"

CPU_INFO_PATH = "/proc/stat"
#CPU_INFO_PATH = "C:\\Users\\admin\\Downloads\\stat"

MEM_INFO_PATH = "/proc/meminfo"
#MEM_INFO_PATH = "C:\\Users\\admin\\Downloads\\meminfo"
