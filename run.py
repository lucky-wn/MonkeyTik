# -*- coding: utf-8 -*-
# @Time : 2020/10/28 上午11:02
# @Author : ning
# @Email : 18301085980@163.com
# @File : run.py.py
# @Software: PyCharm
import subprocess
import time

from model.android import Android
from model.configloader import ConfigLoader
from model.constant import *

# 把日志都移动到LogRepository
subprocess.getoutput("mv %s/* %s" % (result_path, repository_path))

config = ConfigLoader()
loop = int(config.loop)
for l in range(loop):
    print("#\t\t%s Monkey start " % (l + 1))
    TIME = time.strftime("%Y%m%d%H%M%S", time.localtime())
    android = Android(TIME)
    subprocess.getoutput(android.monkey_command)
print("====================测试完成====================")
