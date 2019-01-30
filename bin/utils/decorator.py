# coding: utf-8

import types
import config
import traceback
import logging

from excepts import BaseError, SessionError

from qfcommon.qfpay.qfresponse import QFRET, error
from qfcommon.base.dbpool import get_connection, get_connection_exception

log = logging.getLogger()

# 数据函数dict
data_funcs = {}


def func_register(mode='valid'):
    '''注册接口'''

    def _(func):
        if mode == 'valid':
            data_funcs[func.__name__] = func
        return func

    return _


@func_register()
def user(func):
    def _(self, *args, **kw):
        with get_connection_exception('userdb') as db:
            ret = db.select_one(
                table='session',
                fields='userid, sessionid, state',  # 查询表里的字段名称
                where={'sessionid': self.get_cookie('sessionid')},  # 条件
            )
        if not ret or not ret.get('state'):
            raise SessionError('商户未登录')
        self.userid = ret.get('userid')
        ret = func(self, *args, **kw)
        return ret

    return _


@func_register()
def cate_perm(func):
    '''验证用户角色和权限'''

    def _(self, *args, **kw):
        # 用户角色验证
        if not self.check_cate():
            raise SessionError('用户角色异常')

        # 用户权限验证
        perm_codes = getattr(self, '_perm_codes', None)
        if isinstance(perm_codes, str):
            perm_codes = [perm_codes]

        if not self.check_perms(perm_codes):
            raise SessionError('用户暂无权限操作')

        ret = func(self, *args, **kw)

        return ret

    return _


MulType = (types.ListType, types.TupleType)


def check(funcs=None):
    def _(func):
        def __(self, *args, **kwargs):
            try:
                del_func = func
                deco_funcs = []
                if funcs:
                    deco_funcs = (
                        funcs if isinstance(funcs, MulType) else [funcs]
                    )
                for f in deco_funcs[::-1]:
                    if callable(f):
                        del_func = del_func(f)
                    elif f in data_funcs:
                        del_func = data_funcs[f](del_func)
                return del_func(self, *args, **kwargs)
            except SessionError, e:
                req_method = self.req.method.upper()
                if req_method == 'GET':
                    errinfo = e.errmsg
                    if e.errmsg == '商户未登录':
                        errinfo = ''
                errcode, errinfo = e.errcode, e.errmsg
            except BaseError, e:
                log.warn(traceback.format_exc())
                errcode, errinfo = e.errcode, e.errmsg
            except:
                log.warn(traceback.format_exc())
                errinfo = getattr(self, '_base_err', 'param error')
                errcode = QFRET.PARAMERR

            return error(errcode, errinfo, errinfo)

        return __

    return _


def raise_excp(info='参数错误'):
    def _(func):
        def __(self, *args, **kwargs):
            try:
                # 错误信息
                module_name = getattr(self, '__module__', '')
                class_name = getattr(getattr(self, '__class__', ''), '__name__', '')
                func_name = getattr(func, '__name__', '')
                errinfo = '%s %s %s' % (module_name, class_name, func_name)

                return func(self, *args, **kwargs)
            except BaseError, e:
                log.warn('[%s] error: %s' % (errinfo, e))
                return self.write(error(e.errcode, respmsg=e.errmsg))
            except:
                log.warn('[%s] error:%s' % (errinfo, traceback.format_exc()))
                return self.write(error(QFRET.PARAMERR, respmsg=info))

        return __

    return _
