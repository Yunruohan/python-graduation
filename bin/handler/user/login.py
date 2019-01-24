# coding=utf-8
# -*- coding:utf-8 -*-
# @Time         : 2019/1/14 2:48 PM
# @Description  : 用户登陆登出相关
import uuid
import time
import hashlib

import config
from utils.excepts import ParamError, UserError, DBError
from utils.decorator import check

from qfcommon.web.core import Handler
from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import get_connection, get_connection_exception


class Login(Handler):
    '''用户登录'''

    def POST(self):
        params = self.req.input()       # 接收前端的参数
        fields = ('username', 'password')
        for i in fields:
            if not params.get(i):
                raise ParamError('注册参数不全，缺少{}'.format(i))
        data = {i: params.get(i).strip() for i in fields if params.get(i)}
        # 密码加密
        md = hashlib.md5()  # 构造一个md5对象
        md.update(data.get('password').encode())
        password = md.hexdigest()
        # 数据库查找相关数据校验
        with get_connection_exception('userdb') as db:
            ret = db.select_one(
                table='user',
                fields='id, username, password, state',  # 查询表里的字段名称
                where={'username': data['username']},  # 条件
            )
        if not ret:
            raise ParamError('此账号没有注册，请先注册账号')
        if not ret.get('state'):
            raise ParamError('此账号已被注销，暂不能登陆')
        if ret.get('password') != password:
            raise ParamError('密码不正确')
        # 设置session
        sessionid = str(uuid.uuid4())
        data = {'sessionid': sessionid, 'userid': ret.get('id'), 'create_time': time.strftime('%Y-%m-%d %H:%M:%S')}
        # 数据库存数据
        with get_connection_exception('userdb') as db:
            insert_ret = db.insert(
                table='session',
                values=data
            )
        if not insert_ret:
            raise DBError('insert session data failed')
        self.resp.set_cookie(
            'sessionid', sessionid,
            **config.COOKIE_CONFIG
        )
        ret = {'sessionid': sessionid, 'userid': ret.get('id')}
        return success(ret)


class Logout(Handler):
    '''登出'''

    @check(['user', ])
    def POST(self):
        sesid = self.get_cookie('sessionid')
        with get_connection_exception('userdb') as db:
            update_ret = db.update(
                table='session',
                values={'state': 0},
                where={'sessionid': sesid}      # 条件
            )
        if not update_ret:
            raise DBError('登出失败')
        return success({})