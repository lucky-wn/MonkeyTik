# -*- coding: utf-8 -*-
# @Time : 2020/10/28 下午5:34
# @Author : ning
# @Email : 18301085980@163.com
# @File : collect_performance.py
# @Software: PyCharm
import subprocess
import time
import re
from multiprocessing import Pool
from model.configloader import ConfigLoader

config = ConfigLoader()
TIME_STAMP = time.strftime('%Y%m%d.%H%M%S', time.localtime(time.time()))


class Performance:
    def __init__(self):

        self.serial = config.device
        self.package = config.package
        self.host = config.host
        self.port = config.port
        self.product = "monkey4test"
        self.project = "performance"
        self.now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())

    def get_pid(self):
        """获取进程号"""
        cmd = "adb -s %s shell ps -ef|grep '%s$'|awk '{print $2}'" % (self.serial, self.package)
        pid = subprocess.getoutput(cmd)
        return pid

    def get_upload_sentence(self, performance_type, performance_value):
        """拼接curl句式"""
        now_time = str(time.time()).replace(".", "")
        timestamp_19 = now_time + '0' * (19 - len(now_time))
        sentence = "curl -i -XPOST 'http://%s:%s/write?db=%s' --data-binary '%s,serial=mi2s,type=%s value=%s,start_time_new=%s %s'" \
                   % (self.host, self.port, self.product, self.project, performance_type, performance_value, TIME_STAMP,
                      timestamp_19) + "\n"
        print(performance_type, performance_value)
        print(sentence)
        return sentence

    def upload_sentence_data(self, curl_sentence):
        """上传到数据库"""
        curl_ret = subprocess.getoutput(curl_sentence)
        if curl_ret.find('204 No Content') == -1:
            post_fail_file = open("performance_pfail_%s.txt" % self.now_time, 'a')
            post_fail_file.close()

    def get_performance_parameter(self):
        """获取性能参数，并写入文件"""
        numb = 0
        while numb < 500:
            parameter_file = open("performance_%s.txt" % self.now_time, 'a')
            parameter_file.write(self.get_upload_sentence("cpu", self.get_cpu(self.get_pid())))
            parameter_file.write(self.get_upload_sentence("mem", self.get_mem(self.get_pid())))
            # parameter_file.write()
            # parameter_file.write()
            parameter_file.close()
            numb += 1

    def post_performance_parameter(self):
        """上传性能数据至数据库"""
        s1, s2 = -1, 0
        while s2 > s1:
            time.sleep(10)
            pf = open("performance_%s.txt" % self.now_time, 'rb')
            # 0,从文件开头;1,从当前位置;2,从文件末尾
            pf.seek(s2, 1)
            for le in [line.strip() for line in pf.readlines()]:
                # TODO
                self.upload_sentence_data(le)
            s1 = s2
            s2 = pf.tell()
            pf.close()

    def get_mem(self, pid):
        """获取memory"""
        cmd = "adb shell dumpsys meminfo|grep %s | head -n 1| awk '{print $1}'" % pid
        mem = subprocess.getoutput(cmd)
        return re.sub(r",|K|:", "", mem)

    def get_cpu(self, pid):
        """获取cpu"""
        cmd = "adb shell top -n 1|grep %s|awk '{print $9}'" % pid
        return subprocess.getoutput(cmd)


if __name__ == '__main__':
    pe = Performance()
    pool = Pool(2)
    pool.apply_async(pe.get_performance_parameter, )
    pool.apply_async(pe.post_performance_parameter, )
    pool.close()
    pool.join()
