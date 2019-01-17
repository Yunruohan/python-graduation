# coding=utf-8
# -*- coding:utf-8 -*-
# @Time         : 2018/8/20 下午6:04
# @Description  : The API associated with the small function
import logging
import traceback
import config

from utils.decorator import check
from qfcommon.web.core import Handler
from utils.excepts import ParamError, UserError, DBError

from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import get_connection, get_connection_exception

log = logging.getLogger()


class InsertHandler(Handler):
    '''存数据'''

    @check(['user', ])
    def POST(self):
        params = self.req.input()       # 接收前端的参数
        # 数据库存数据
        with get_connection('qf_org') as db:    # 括号里的是数据库名称
            insert_ret = db.insert(
                table='qd_profile',             # 表名称
                values=params                   # 存数据库的值，字典形式，键值对和表字段一致，只能少不能多
            )
        if not insert_ret:
            raise DBError('save data failed')
        return success('成功')


class EditHandler(Handler):
    '''修改数据'''

    @check(['user', ])
    def POST(self):
        params = self.req.input()       # 接收前端的参数
        uid = params.get('uid')
        # 数据库存数据
        with get_connection('qf_org') as db:
            update_ret = db.update(
                table='qd_profile',
                values=params,
                where={'uid': uid}      # 条件
            )
        if not update_ret:
            raise DBError('update data failed')
        return success('成功')


class InfoHandler(Handler):
    '''查看数据'''

    @check(['user', ])
    def POST(self):
        params = self.req.input()       # 接收前端的参数
        uid = params.get('uid')
        # 数据库存数据
        with get_connection('qf_org') as db:
            update_ret = db.select_one(
                table='qd_profile',
                fields='uid, memo',     # 查询表里的字段名称
                where={'uid': uid},   # 条件
            )
        if not update_ret:
            raise DBError('update data failed')
        return success('成功')