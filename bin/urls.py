# coding:utf-8

from handler.demo import demo_handler
from handler.user import registered

urls = (
    # 功能类接口
    (r'^/demo/insert$', demo_handler.InsertHandler),   # 存数据
    (r'^/demo/edit$', demo_handler.EditHandler),   # 修改数据
    (r'^/demo/info$', demo_handler.InfoHandler),   # 查看数据

    # 用户相关
    (r'^/user/register$', registered.Register),   # 用户注册

)

