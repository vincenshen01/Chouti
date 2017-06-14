# -*- coding:utf-8 -*-
# @Time     : 2017-06-06 12:55
# @Author   : gck1d6o
# @Site     : 
# @File     : tags.py
# @Software : PyCharm

import re
from django import template
from datetime import datetime


register = template.Library()


@register.filter
def url_filter(url):
    regex = re.compile(r"^(http|https).+\.(com|cn|org)/")
    result = regex.match(url)
    if result:
        return result.group()


@register.filter
def time_filter(time):
    seconds = datetime.now().timestamp() - time.timestamp()
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d > 0:
        return ("%s天%s小时" %(int(d), int(h)))
    elif h > 0:
        return ("%s小时%s分钟" %(int(h), int(m)))
    else:
        return ("%s分钟" %int(m))