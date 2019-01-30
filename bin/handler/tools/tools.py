# coding=utf-8
# -*- coding:utf-8 -*-
# @Time         : 2019/1/28 4:20 PM
# @Description  :
import os
import time
import uuid
import imghdr
import config

from utils.excepts import ParamError, UserError, DBError
from utils.decorator import check

from qfcommon.web.core import Handler
from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import get_connection, get_connection_exception


class UploadPictures(Handler):
    '''上传图片'''

    @check(['user', ])
    # @check()
    def POST(self):
        files = self.req.files()
        if not files:
            raise ParamError('未获取到文件')
        fs = files[0]
        # 图片后缀名
        ext_name = os.path.splitext(fs.filename)[1].lower()
        if not ext_name:
            file_type = imghdr.what(fs.file)
            if file_type == 'jpg' or file_type == 'jpeg':
                ext_name = '.jpg'
            elif file_type == 'png':
                ext_name = '.png'
        if ext_name == '.jpeg':
            ext_name = '.jpg'

        if ext_name not in ('.jpg', '.png'):
            raise ParamError('不支持该图片格式')
        content = fs.file.read()
        dir_name = os.path.join(config.SAVE_PICTURES_URL, str(self.userid))
        if os.path.isdir(dir_name):
            pass
        else:
            os.mkdir(dir_name)
        name = str(uuid.uuid1()) + ext_name
        url = os.path.join(dir_name, name)
        with open(url, 'wb') as f:
            f.write(content)
        data = {}
        data['userid'] = self.userid
        data['url'] = name
        data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        with get_connection_exception('userdb') as db:
            insert_ret = db.insert(
                table='picture_record',
                values=data
            )

        if not insert_ret:
            raise DBError('insert user data failed')
        url = os.path.join(config.BASE_URL, str(self.userid), name)
        return success({'url': url})


class ShowPictures(Handler):
    '''展示图片'''

    @check(['user', ])
    def GET(self):
        pictures = []
        with get_connection_exception('userdb') as db:
            ret = db.select(
                table='picture_record',
                where={'userid': self.userid},  # 条件
            )
        if not ret:
            return success(pictures)
        # 构造url
        for i in ret:
            url = os.path.join(config.BASE_URL, str(self.userid), i['url'])
            pictures.append({'name': i.get('name'), 'create_time': i.get('create_time'), 'url': url})
        return success(pictures)
