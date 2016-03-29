#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
import os, time, urllib2, json
from utils import utils
from utils.DBMysql import gm
from fuzzle.scanIssue import scanIssue
from fuzzle import vulTypes

class sqliAudit():
    def __init__(self, drequest):
        #self.sqlmapip = "182.92.191.201"
        self.dreq = drequest
        self.host = drequest.host
        self.url = drequest.url
        self.method = drequest.method
        self.sqlmapip = "127.0.0.1"
        self.sqlmapport = "8775"
        self.server = 'http://' + self.sqlmapip + ':' + self.sqlmapport
        self.tmp_dir = "d:\\tmp"
        self.request = drequest.request
        self.request_file = ""
        self.sqlitaskid = ""
        self.isVul = False
        self.result = {}

    
    def __task_new(self):
        try:
            req = urllib2.Request( self.server+ '/task/new')
            resp = json.load(urllib2.urlopen(req))
            if resp['success'] == True:
                self.sqlitaskid = resp['taskid']
                self.request_file = self.tmp_dir+"\\"+self.sqlitaskid
                utils.write_file(self.request_file, self.request)
                print 'Created SQLMap Task: ' + self.sqlitaskid + '\n'
            else:
                print 'SQLMap task creation failed\n'
        except:
            print 'Except SQLMap task creation failed\n'
    
    
    def __option_set(self):
        #self.sqliopts = {'requestFile': self.request_file, "smart": True}
        self.sqliopts = {'requestFile': self.request_file}
        try:
            req = urllib2.Request(self.server + '/option/' + self.sqlitaskid + '/set')
            req.add_header('Content-Type', 'application/json')
            req.add_header('Cache-Control', 'nocache')
            req.add_header('Pragma', 'no-cache')
            req.add_header('Expires', '-1')

            resp = json.load(urllib2.urlopen(req, json.dumps(self.sqliopts)))
                
            if resp['success'] == True:
                print 'SQLMap options set on Task ' + self.sqlitaskid + ': ' + json.dumps(self.sqliopts) + '\n' 
        except:
            print 'Except SQLMap task option set failed\n'  
             
    
    def __option_list(self):
        try:
            checkreq = urllib2.Request(self.server + '/option/' + self.sqlitaskid + '/list')
            checkresp = json.load(urllib2.urlopen(checkreq))
            print 'SQLMap options returned: ' + json.dumps(checkresp) + '\n'
        except:
            print 'Failed to get list of options from SQLMap API\n'
    
    def __task_start(self):
        try:
            req = urllib2.Request(self.server + '/scan/' + self.sqlitaskid + '/start')
            req.add_header('Content-Type', 'application/json')
            resp = json.load(urllib2.urlopen(req, json.dumps(self.sqliopts)))
            if resp['success'] == True:
                print 'Started SQLMap Scan on Task ' + self.sqlitaskid +' with Engine ID: ' + str(resp['engineid']) + '\n'
                print json.dumps(resp)
            else:
                print 'Failed to start SQLMap Scan for Task: ' + self.sqlitaskid + '\n'
        except:
            print 'Except Failed to start SQLMap Scan for Task: ' + self.sqlitaskid + '\n'
    def __scan_status(self):
        time.sleep(5)
        while True:
            try:
                req = urllib2.Request(self.server + '/scan/' + self.sqlitaskid + '/status')
                req.add_header('Content-Type', 'application/json')
                resp = json.load(urllib2.urlopen(req))
                print json.dumps(resp)
                if resp['status'] == "running":
                    print 'Scan for task '+self.sqlitaskid+' is still running.\n'
                elif resp['status'] == "terminated":
                    if resp['returncode'] == 0:
                        print 'Scan for task '+self.sqlitaskid+' completed.  Gathering results.\n'
                    utils.del_file(self.request_file)
                    break
                time.sleep(5)
            except Exception as err:
                print (err)
    
    def __scan_data(self):                                       
        try:
            req = urllib2.Request(self.server + '/scan/' + self.sqlitaskid + '/data')
            req.add_header('Content-Type', 'application/json')
            resp = json.load(urllib2.urlopen(req))
            
            print json.dumps(resp)
            self.__analysis_data(resp['data'])
        except:
            pass
        
    def __analysis_data(self, data):
        self.__init_result()
        for data in data:
            self.isVul = True
            print data
            if data['type'] == 0:
                if isinstance(data['value'][0]['dbms'], list):
                    for dbtypes in data['value'][0]['dbms']:
                        self.result['dbtype'] = self.result['dbtype'] + dbtypes + ', or '
                    self.result['dbtype'] = self.result['dbtype'][:-5]
                else:
                    self.result['dbtype'] = data['value'][0]['dbms']
                
                self.result['parameter'] = data['value'][0]['parameter']
                
                for items in data['value']:
                    for k in items['data']:
                        self.result['payloads'] = self.result['payloads'] +items['data'][k]['payload']+'\r\n'
                        
                self.result['payloads'].rstrip('\r\n')
                
        print self.result
    
    def __insertVul(self):
        vul = scanIssue(rid=self.dreq.rid, type= vulTypes.sql, host= self.host, url= self.url, method=self.method, parameters=self.result['parameter'], payload= self.result['payloads'])
        gm.insertVul(vul)
              
    def __init_result(self):
        self.result['dbtype'] = ''
        self.result['payloads'] = ''
        self.result['parameter'] = ''
        '''
        self.result['banner'] = ''
        self.result['cu'] = ''
        self.result['hostname'] = ''
        self.result['cdb'] = ''
        self.result['isdba'] = ''
        self.result['lusers'] = ''
        self.result['lprivs'] = ''
        self.result['lroles'] = ''
        self.result['ldbs'] = ''
        self.result['lpswds'] = ''
        '''

    def __task_stop(self):
        pass
            
    def audit(self):
        #request_file = "d:\\dvwa-sqli.txt"  
        self.__task_new()
        self.__option_set()
        #self.__option_list()
        self.__task_start()
        self.__scan_status()
        self.__scan_data()
        print "--------------------"+self.result['parameter']
        if self.result['parameter']:
            self.__insertVul()
                              
                    
def getPluginClass():
    return sqliAudit          
                
if __name__ == '__main__':
    '''
    drequest = {"brequest":[71,69,84,32,47,115,113,108,105,46,112,104,112,63,110,97,109,101,61,122,104,97,110,103,113,105,110,38,112,119,100,61,53,51,51,55,51,57,53,56,32,72,84,84,80,47,49,46,49,13,10,72,111,115,116,58,32,97,117,116,111,46,99,111,109,13,10,85,115,101,114,45,65,103,101,110,116,58,32,77,111,122,105,108,108,97,47,53,46,48,32,40,87,105,110,100,111,119,115,32,78,84,32,54,46,51,59,32,87,79,87,54,52,59,32,114,118,58,51,56,46,48,41,32,71,101,99,107,111,47,50,48,49,48,48,49,48,49,32,70,105,114,101,102,111,120,47,51,56,46,48,13,10,65,99,99,101,112,116,58,32,116,101,120,116,47,104,116,109,108,44,97,112,112,108,105,99,97,116,105,111,110,47,120,104,116,109,108,43,120,109,108,44,97,112,112,108,105,99,97,116,105,111,110,47,120,109,108,59,113,61,48,46,57,44,42,47,42,59,113,61,48,46,56,13,10,65,99,99,101,112,116,45,76,97,110,103,117,97,103,101,58,32,122,104,45,67,78,44,122,104,59,113,61,48,46,56,44,101,110,45,85,83,59,113,61,48,46,53,44,101,110,59,113,61,48,46,51,13,10,65,99,99,101,112,116,45,69,110,99,111,100,105,110,103,58,32,103,122,105,112,44,32,100,101,102,108,97,116,101,13,10,67,111,110,110,101,99,116,105,111,110,58,32,107,101,101,112,45,97,108,105,118,101,13,10,13,10],"completed":True,"hasBodyParam":False,"hasCookieParam":False,"hasQueryStringParam":True,"hasSetCookies":False,"host":"auto.com","method":"GET","protocol":"http","referrerURL":"","request":"GET /sqli.php?name=zhangqin&pwd=53373958 HTTP/1.1\r\nHost: auto.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n","requestLength":1426,"requstContentType":"HTML","responseContentType":"text/html","responseContentType_burp":"HTML","responseInferredContentType_burp":"","responseLength":0,"responseTime":"","status":200,"targetPort":80,"url":"http://auto.com:80/sqli.php?name=zhangqin&pwd=53373958","urlExtension":"php"}
    print drequest["request"]
    print drequest["host"]
    print drequest["url"]
    print drequest["method"]
    
    sqliAudit(drequest).audit()
    '''
    from utils.pluginsManager import pm
    from utils.GRedis import gredis
    from fuzzle.grequest import DRequest
    
    dreq = gredis.getTask() 
            
    if dreq:
        dreq = DRequest(dreq)
        print dir(dreq)
        xss = sqliAudit(dreq)
        xss.audit()
        #pm.run(dreq)
    


