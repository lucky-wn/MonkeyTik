# -*- coding: utf-8 -*-
# @Time : 2020/10/28 上午11:33
# @Author : ning
# @Email : 18301085980@163.com
# @File : Android.py
# @Software: PyCharm
import subprocess
import os

from model.configloader import ConfigLoader
from model.constant import *


config = ConfigLoader()


class Android:

    def __init__(self, TIME):
        self.exec_time = TIME
        self.monkey_command = "adb -s %s shell monkey -p %s --throttle %s %s " % (config.device, config.package, config.throttle, config.log)
        pct_cmd = ["--pct-touch", "--pct-motion", "--pct-rotation", "--pct-nav", "--pct-majornav", "--pct-syskeys"]
        if config.pct:
            for idx, value in enumerate(config.pct):
                if value is not "0":
                    self.monkey_command += pct_cmd[idx] + " " + value + " "
        if config.ignore_crashes:
            self.monkey_command += " --ignore-crashes "
        if config.ignore_native_crashes:
            self.monkey_command += " --ignore-native-crashes "
        if config.ignore_timeouts:
            self.monkey_command += " --ignore-timeouts "
        self.monkey_command += config.exec_times
        self.monkey_command += " >> %s" % result_path + os.sep + "mokey_%s.log" % self.exec_time


if __name__ == '__main__':
    print(subprocess.getoutput("export PATH=$PATH:/home/it/env/android-sdk-linux/platform-tools"))
    ad = Android()
    print(ad.monkey_command)
    ret = subprocess.getoutput(ad.monkey_command)
    print(ret)
