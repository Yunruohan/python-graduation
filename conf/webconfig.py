# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import os
import sys
HOME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin')
from qfcommon.web.middleware import JSONPMiddleware

# URLS配置
URLS = None

# 静态路径配置
STATICS = {'/static/': '/static/'}

# 模板配置
TEMPLATE = {
    'cache': True,
    'path': 'templates',
    'tmp': os.path.join(HOME, '../tmp'),
}

# APP就是一个子目录
APPS = (

)

# 中间件
MIDDLEWARE = (
    # middleware
    JSONPMiddleware,
)

# WEB根路径
DOCUMENT_ROOT = HOME

# 页面编码
CHARSET = 'UTF-8'

# session配置
SESSION = {'store': 'DiskSessionStore', 'expire': 30, 'path': '/tmp'}
