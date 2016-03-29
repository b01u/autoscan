#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
import json, urlparse
from utils.DBMysql import gm
from utils.GLog import elog, getDlog

class DRequest(object):
    def __init__(self, drequest):
        self.dlog = getDlog(__name__)
        self.dreq = json.loads(drequest)
        self.dealRequest()
        self.dealUrl()
        self.dealHeaders()
        self.insertMysql()
        #self.dlog.debug("[Fuzzle Request] %s"%str(drequest))
        self.dlog.debug("[Fuzzle Request] %s"%str(self.url))
        
    def dealRequest(self, dreq = ""):
        self.dreq = dreq if dreq else self.dreq
        self.url = self.dreq["url"]
        self.host = self.dreq["host"]
        self.method = self.dreq["method"]
        self.postdata = self.dreq["postdata"]
        self.request = self.dreq["request"]
        self.brequest = self.dreq["brequest"]

    
    def dealHeaders(self):
        self.headers = dict()
        self.cookie = ""
        for h in self.dreq["headers"]:
            if h.startswith("POST") or h.startswith("GET"):
                continue
            else:
                paire =  h.split(":")
                if h.startswith("Cookie"):
                    self.cookie =paire[1]
                try:
                    self.headers[paire[0]] = paire[1]
                except:
                    pass
    
    def dealUrl(self):
        up = urlparse.urlparse(self.url)
        if up.query:
            self.path = up.path+"?"+up.query
        else:
            self.path = up.path
            
    def insertMysql(self):
        self.rid =  gm.insertRequest(self)
