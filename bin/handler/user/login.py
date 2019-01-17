# coding=utf-8
# -*- coding:utf-8 -*-
# @Time         : 2019/1/14 2:48 PM
# @Description  : 用户登陆登出相关
from utils.excepts import ParamError, UserError, DBError

from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import get_connection, get_connection_exception

class LOGIN():
    '''用户登录'''

    def POST(self):
        params = self.req.input()       # 接收前端的参数
        name = params.get('name')
        password = params.get('password')
        # 数据库存数据
        with get_connection('gbb') as db:
            update_ret = db.update(
                table='users',
                values=params
            )
        if not update_ret:
            raise DBError('update data failed')
        return success('成功')