#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
import copy
'''
requests:
    urlpath
    postdata
'''
class fuzzleRequests():
    def __init__(self, urlpath, postdata , payloads):
        self.urlpath = urlpath
        self.postdata = postdata
        self.payloads = payloads
        self.drequests = {}

        if self.urlpath.find("?") >= 0:
            self.path, self.query_params = self.urlpath.split("?")
        
    #根据参数fuzzle
    def fuzzleParams(self, query_params=""):
        query_params =  query_params if query_params else self.query_params 
        query_paires =  query_params.split("&") if query_params.find("&") >= 0 else [query_params, ]

        fuzzle_params = []
        for i in range(len(query_paires)):
            for payload in self.payloads:
                tmp_query_paire = copy.copy(query_paires)
                tmp_params = query_paires[i].split('=')
                tmp_fuzzle_key, tmp_params[1] = tmp_params[0], tmp_params[1] + payload
                tmp_query_paire[i] = '='.join(tmp_params)
                fuzzle_query_param = '&'.join(tmp_query_paire)
                fuzzle_params.append({"fuzzle_key": tmp_fuzzle_key, "fuzzle_query_param": fuzzle_query_param, "payload": payload})
                
        return fuzzle_params
    
    def __getFuzzleRequests(self, fuzzle_params, isPost = False):
        for i in range(len(fuzzle_params)):
            fuzzle_request = {}
            fuzzle_key = fuzzle_params[i]["fuzzle_key"]
            if not fuzzle_key in self.drequests.keys():
                self.drequests[fuzzle_key] = [] 
            fuzzle_request["url"] = self.path + '?' + fuzzle_params[i]["fuzzle_query_param"] if isPost is False else self.urlpath
            fuzzle_request["postdata"] = self.postdata if isPost is False else fuzzle_params[i]["fuzzle_query_param"]
            fuzzle_request["payload"] = fuzzle_params[i]["payload"]
            
            self.drequests[fuzzle_key].append(fuzzle_request)
                                     
    #fuzzle的参数加入requests当中
    def getFuzzleRequests(self):  
        if self.urlpath.find("?") >= 0:
            fuzzle_params = self.fuzzleParams()
            self.__getFuzzleRequests(fuzzle_params)
           
        if self.postdata:
            postdatas = self.fuzzleParams(self.postdata)
            self.__getFuzzleRequests(postdatas, True)

        return self.drequests
    
if __name__ == "__main__":
    from fuzzle.payloads import xssPayloads
    
    xssfuzzleRequests = fuzzleRequests("test1.php", "age=xxx&toal=fff", xssPayloads.payloads)
    
    xss = xssfuzzleRequests.getFuzzleRequests()
    
    for x,y in xss.items():
        print x
        print y
        
    dd = {"name" :"zhangqin", "pass": "sksks"}
    #print "name" in dd.keys()
        
    
    