#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from utils.pluginsManager import pm
from utils.GRedis import gredis
from fuzzle.grequest import DRequest
from utils.GLog import elog, getDlog
import time, sys

class QScan(object):
    def __init__(self):
        self.dlog = getDlog(__name__)
    def run(self): 
        while 1:
            rreq = gredis.getTask() 
            if rreq:
                dreq = DRequest(rreq)
                self.dlog.debug("[New Tasker] url:%s"%str(dreq.url))
                pm.run(dreq)
            else:
                print "Redis don't have request"
                time.sleep(5)
        
if __name__ == "__main__":
    try:
        qscan = GJScan()
        qscan.run()
    except KeyboardInterrupt :
        sys.exit(0)
    except Exception,e:
        elog.exception(e)
