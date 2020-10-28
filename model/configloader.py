# -*- coding: utf-8 -*-
# @Time : 2020/10/28 上午11:13
# @Author : ning
# @Email : 18301085980@163.com
# @File : configloader.py
# @Software: PyCharm
import configparser
from model.constant import *


class ConfigLoader:
    """
    读取配置文件
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding="utf-8")
        # 命令参数
        self.package = self.config.get("command", "package")
        self.throttle = self.config.get("command", "throttle")
        self.pct = self.config.get("command", "pct").split("/")
        self.ignore_crashes = self.config.get("command", "ignore_crashes")
        self.ignore_timeouts = self.config.get("command", "ignore_timeouts")
        self.ignore_native_crashes = self.config.get("command", "ignore_native_crashes")
        self.log = self.config.get("command", "log")
        self.exec_times = self.config.get("command", "exec_times")
        self.loop = self.config.get("command", "loop")
        # app参数
        self.app_install_path = self.config.get("app", "app_path")
        self.app_version = self.config.get("app", "app_version")
        self.device = self.config.get("app", "device")
        # grafana service
        self.host = self.config.get("service", "host")
        self.port = self.config.get("service", "port")
        self.update_datas = self.config.get("service", "update_datas")
        self.measurement_name = self.config.get("service", "measurement_name")


if __name__ == '__main__':
    config = ConfigLoader()
    print(config.package)
    print(config.throttle)
    print(config.pct)
    print(config.ignore_crashes)
    print(config.ignore_timeouts)
    print(config.ignore_navtive_crashes)
    print(config.app_install_path)
    print(config.app_version)
    print(config.host)
    print(config.port)
    print(config.update_datas)
    print(config.measurement_name)
