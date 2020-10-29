# -*- coding: utf-8 -*-
# @Time : 2020/10/28 下午5:34
# @Author : ning
# @Email : 18301085980@163.com
# @File : collect_performance.py
# @Software: PyCharm
import subprocess
import time
from threading import Thread
from model.configloader import ConfigLoader

config = ConfigLoader()
TIME_STAMP = time.strftime('%Y%m%d.%H%M%S', time.localtime(time.time()))
"""
curl -i -XPOST 'http://localhost:8086/write?db=monkey4test' --data-binary 
'performance,serial=mi2s,type=cpu value=16,start_time_new=20201028.182448 1603880702905377900'
"""


class Performance:
    def __init__(self):

        self.serial = config.device
        self.package = config.package
        self.host = config.host
        self.port = config.port
        self.product = "monkey4test"
        self.project = "performance"

    def get_pid(self):
        """获取进程号"""
        cmd = "adb -s %s shell ps -ef|grep '%s$'|awk '{print $2}'" % (self.serial, self.package)
        pid = subprocess.getoutput(cmd)
        return pid

    def upload_sentence(self, performance_type, performance_value):
        now_time = str(time.time()).replace(".", "")
        timestamp_19 = now_time + '0' * (19 - len(now_time))
        sentence = "curl -i -XPOST 'http://%s:%s/write?db=%s' --data-binary '%s,serial=mi2s,type=%s value=%s,start_time_new=%s %s'" \
                   %(self.host, self.port, self.product, self.project, performance_type, performance_value, TIME_STAMP, timestamp_19)
        return sentence

    def get_cpu(self, pid):
        """获取cpu"""
        cmd = "adb shell top -n 1|grep %s|awk '{print $9}'" % pid
        return subprocess.getoutput(cmd)

    def get_performance_parameter(self):
        app_pid = self.get_pid()
        performance_value = self.get_cpu(app_pid)
        sen = self.upload_sentence("cpu", performance_value)
        print(sen)
        subprocess.getoutput(sen)


if __name__ == '__main__':
    pe = Performance()
    while True:
        pe.get_performance_parameter()
