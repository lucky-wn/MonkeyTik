# -*- coding: utf-8 -*-
# @Time : 2020/10/28 下午5:34
# @Author : ning
# @Email : 18301085980@163.com
# @File : collect_performance.py
# @Software: PyCharm
from threading import Thread
from model.configloader import ConfigLoader

config = ConfigLoader()


class Performance:
    def __init__(self):

