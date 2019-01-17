# coding:utf-8

import os
from webconfig import *

# 服务地址
HOST = '0.0.0.0'

# 服务端口
PORT = 6100

DEBUG = False

# 日志文件配置
# LOGFILE = os.path.join(HOME, '../log/project.log')
LOGFILE = 'stdout'

# 数据库配置
DATABASE = {
    'gbb': {
        'engine': 'pymysql',
        'db': 'gbb',
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '12345678',
        'charset': 'utf8',
        'conn': 16,
    },
}

# cookie配置
COOKIE_CONFIG = {
    'max_age': 86400,
    'domain': None,
}

# redis配置
REDIS_CONF = {
    'host': '172.100.101.107',
    # 'host': '172.100.101.106',
    'port': 6379,
    'password': '',
    # 'default_expire' : 2 * 24 * 60 * 60
}