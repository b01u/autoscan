#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from utils.DBMysql import gm

class scanIssue(object):
    def __init__(self, rid, type, host, url, method, parameters, payload):
        self.rid = rid
        self.type = type
        self.host = host
        self.url = url
        self.method = method
        self.parameters = parameters
        self.payload = payload
        
    def insertMysql(self):
        gm.insertVul(self)
        
    def __repr__(self):
        return "rid : %s -- type: %s -- parameters : %s "%(self.rid, self.type, self.parameters)
        
if __name__ == "__main__":
    from fuzzle import vulTypes
    s = scanIssue("1", vulTypes.sql, ["name", "passwd"], "ssss")
    print s
        
    
    