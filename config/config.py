#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from ConfigParser import ConfigParser
import os

class Config(ConfigParser):
    filename = os.path.dirname(__file__)+os.path.sep+"config.ini"
    def __init__(self):
        ConfigParser.__init__(self)
        self.read(self.filename)
        #redis相关配置
        self.redis_host = self.get("redis", "host")
        self.redis_port = self.getint("redis", "port")
        #mysql相关配置
        self.mysql_host = self.get("mysql", "host")
        self.mysql_port = self.getint("mysql", "port")
        self.mysql_db = self.get("mysql", "db")
        self.mysql_user = self.get("mysql", "user")
        self.mysql_pass = self.get("mysql", "pass")
        #sqlmap相关配置
        self.sqlmap_path = self.get("sqlmap", "path")
        self.sqlmap_tmppath = self.get("sqlmap", "tmppath")

cf = Config()        
if __name__ == "__main__":
    print cf.get("redis", "host") 
    print cf.redis_host
