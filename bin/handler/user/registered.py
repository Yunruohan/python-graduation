# coding=utf-8
# -*- coding:utf-8 -*-
# @Time         : 2019/1/14 2:54 PM
# @Description  : 用户注册相关
from utils.excepts import ParamError, UserError, DBError

from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import get_connection, get_connection_exception

class REGISTER():
    '''用户注册'''

    def POST(self):
        params = self.req.input()       # 接收前端的参数
        # 数据库存数据
        with get_connection('sd') as db:
            update_ret = db.update(
                table='user',
                values=params
            )
        if not update_ret:
            raise DBError('update data failed')
        return success('成功')