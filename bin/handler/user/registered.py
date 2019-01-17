# coding=utf-8
# -*- coding:utf-8 -*-
# @Time         : 2019/1/14 2:54 PM
# @Description  : 用户注册相关
import re
import time
import string
import hashlib

from utils.excepts import ParamError, UserError, DBError

from qfcommon.web.core import Handler
from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import get_connection, get_connection_exception


re_email = re.compile(r'^([a-zA-Z\.0-9]+)@[a-zA-Z0-9]+\.[a-zA-Z0-9]{3}$')

# 判断只有字母数字
def just_letters_int_func(s):
    range_in = string.digits + string.ascii_letters
    for i in s:
        if i not in range_in:
            raise ValueError


class Register(Handler):
    '''用户注册'''

    def POST(self):
        params = self.req.input()       # 接收前端的参数
        # 校验数据
        data = self._check_params(params)
        # 密码加密
        md = hashlib.md5()  # 构造一个md5对象
        md.update(data.get('password').encode())
        password = md.hexdigest()
        data['password'] = password
        data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        # 数据库存数据
        with get_connection('gbb') as db:
            insert_ret = db.insert(
                table='user',
                values=data
            )

        if not insert_ret:
            raise DBError('insert data failed')
        with get_connection('gbb') as db:
            ret = db.select_one(
                table='user',
                fields='id',  # 查询表里的字段名称
                where={'username': data['username']},  # 条件
            )
        return success({'userid': ret['id']})

    def _check_params(self, params):
        '''校验数据'''
        if not params:
            raise ParamError('注册参数不能为空')
        fields = ('username', 'password')
        for i in fields:
            if not params.get(i):
                raise ParamError('注册参数不全，缺少{}'.format(i))
        data = {i: params.get(i).strip() for i in fields if params.get(i)}
        try:
            just_letters_int_func(data.get('password'))
        except:
            raise ParamError('密码只能是字母或数字')
        # 账号做两种类型，字母或数字、邮箱
        if '@' in data.get('username'):
            if not re_email.match(data.get('username')):
                raise ParamError('邮箱格式不对')
        else:
            try:
                just_letters_int_func(data.get('username'))
            except:
                raise ParamError('账号格式不正确')
        return data