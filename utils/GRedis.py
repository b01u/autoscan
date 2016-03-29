#/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from sys import path
from os.path import dirname, abspath
path.append( dirname(dirname(abspath(__file__))) )
import redis
from config.config import cf
from GLog import elog, getDlog

class GRedis(object):
    def __init__(self):
        self.dlog = getDlog(__name__)
        try:
            self.redis = redis.StrictRedis(host=cf.redis_host, port=cf.redis_port, db=0)
        except Exception,e:
            elog.exception(e)
    def getKeys(self, patter = "*"):
        return self.redis.keys(patter) 
    
    def getTask(self):
        l = self.redis.lpop("lrequests")
        #l = l if l else self.redis.lpop("auto.com")
        return l
    
gredis = GRedis()

if __name__ == "__main__":
    print gredis.getKeys()   
    print gredis.redis.lpop("auto.com")     
    print gredis.getKeys()   
