# encoding:utf-8

import config
import redis

from config import REDIS_CONF
from qfcommon.web import cache as qf_cache
qfcache = qf_cache.install()

# redis连接池
redis_pool = redis.Redis(**REDIS_CONF)
