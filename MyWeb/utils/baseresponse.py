# -*- coding:utf-8 -*-
# @Time     : 2017-06-06 10:05
# @Author   : gck1d6o
# @Site     : 
# @File     : baseresponse.py
# @Software : PyCharm


class AjaxResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.error = None
        self.index = False