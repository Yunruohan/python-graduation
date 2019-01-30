# coding:utf-8

from handler.user import registered
from handler.user import login
from handler.tools import tools

urls = (
    # 用户相关
    (r'^/user/register$', registered.Register),   # 用户注册
    (r'^/user/login$', login.Login),   # 用户登陆
    (r'^/user/logout$', login.Logout),   # 用户登出

    (r'^/pictures/upload$', tools.UploadPictures),   # 上传图片
    (r'^/pictures/show$', tools.ShowPictures),   # 展示图片

)

