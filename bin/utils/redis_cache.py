# coding:utf-8

'''
用redis作缓存
'''

try:
    import simplejson as json
except:
    import json

import config
import logging
import traceback

from runtime import redis_pool

from qfcommon.qfpay.qfresponse import json_default_trans

log = logging.getLogger()

prefix = getattr(
    config, 'REDIS_CACHE_PREFIX', 'org_slsm'
)


class RedisCache(object):
    '''redis缓存'''

    def __init__(self, update_func, timeout=60*10):
        self._update_func = update_func
        self._timeout = timeout
        self._prefix = '.'.join([
            prefix, update_func.__module__,
            update_func.__class__.__name__,
            update_func.__name__
        ])

    def __getitem__(self, key):
        '''获取缓存'''
        rkey = self._prefix+str(key)
        try:
            return json.loads(redis_pool.get(rkey))
        except:
            pass

        ret = None
        try:
            ret = self._update_func(key)

            redis_pool.setex(
                rkey, json.dumps(ret, default=json_default_trans),
                self._timeout
            )
        except:
            log.warn(traceback.format_exc())

        return ret

    def delete(self, keys):
        '''删除缓存'''
        rkeys = [self._prefix + str(i) for i in keys]
        redis_pool.delete(*rkeys)
