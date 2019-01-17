# coding:utf-8

import re
import time
import json
import datetime
import string
import logging
log = logging.getLogger()

from functools import partial

from constants import BaseDef

re_mobile = re.compile(BaseDef.MOBILE_PATTERN)

def is_valid(s, func):
    try:
        func(s)
        return True
    except:
        return False

# 判断是否是日期
is_valid_date = partial(is_valid, func=lambda s: time.strptime(s, BaseDef.DATE_FMT))

# 判断是否是时间
is_valid_datetime = partial(is_valid, func=lambda s: time.strptime(s, BaseDef.DATETIME_FMT))

# 判断是否是数字
is_valid_num = partial(is_valid, func=float)

# 判断是否是整形
is_valid_int = partial(is_valid, func=int)

# 判断是否是float
is_valid_float = partial(is_valid, func=float)

# 判断是否能json.dumps
is_valid_json = partial(is_valid, func=json.dumps)

# 判断是否能json.loads
is_valid_loads = partial(is_valid, func=json.loads)

# 判断是否datetime
def is_date_type(v):
    return isinstance(v, (datetime.date, datetime.time))

# 判断是否是手机号
def is_valid_mobile(v):
    return re_mobile.match(v)

# 判断只有字母数字
def just_letters_int_func(s):
    range_in = string.digits + string.ascii_letters
    for i in s:
        if i not in range_in:
            raise ValueError
just_letters_int = partial(is_valid, func=just_letters_int_func)


# 校验中文
def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

