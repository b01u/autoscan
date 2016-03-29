#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from sys import path
from os.path import dirname, abspath
path.append( dirname(dirname(abspath(__file__))) )
import urlparse, requests, time, urllib
from PySide import QtWebKit
from fuzzle.fuzzleRequests import fuzzleRequests 
from fuzzle.payloads import xssPayloads
from fuzzle.scanIssue import scanIssue
from utils.DBMysql import gm
from fuzzle import vulTypes
from utils.GLog import elog, getDlog
from utils.besm import besm
from utils.browser import QBrowser
from colorama import init, Fore
init(autoreset = True )


class XssWebPage(QtWebKit.QWebPage):
        def __init__(self, app):
            super(XssWebPage, self).__init__(app)
            self.xss = False

        def javaScriptAlert(self, frame, msg):
            if msg == xssPayloads.fuzzle_msg:
                self.xss = True
                print "There is a xss :"+msg
            #print "on alert:"+msg

        def setUserAgent(self, user_agent):
            self.user_agent = user_agent

class rxssAudit(fuzzleRequests):
    def __init__(self, drequest):
        self.dreq = drequest
        self.url = drequest.url
        up = urlparse.urlparse(self.url)
        self.host = up.scheme+"://"+up.netloc
        if up.query:
            self.urlpath = up.path+"?"+up.query
        else:
            self.urlpath = up.path
        
        self.headers = drequest.headers
        self.xpostdata = drequest.postdata
        self.vul_params = []
        self.vpayloads = []
        self.dlog = getDlog(__name__)
        self.insertVul = lambda scanissue: gm.insertVul(scanissue)
        self.__esm = besm(xssPayloads.payloads)
        self.browser = QBrowser(web_page_class=XssWebPage)
        fuzzleRequests.__init__(self, self.urlpath, self.xpostdata, xssPayloads.payloads)
        print self.headers
        
    #xss 检测  
    def audit(self):
        xss_fuzzle_requests = self.getFuzzleRequests()
        print "all request => " + str(xss_fuzzle_requests)
        for k,v in xss_fuzzle_requests.items():
            for request  in v:
                if k not in self.vul_params:
                    xurl = self.host+request["url"]
                    method = "get" if not request["postdata"] else "post"
                    print "the url is =>" + xurl
                    print "the method is => "+method
                    print "postdata => "+str(request["postdata"])
                    try:
                        '''
                        if not request["postdata"]:
                            self.browser.
                            #resp = requests.get(xurl, headers=self.headers)
                        else:
                            self.headers["Content-Type"] = "application/x-www-form-urlencoded"
                            resp = requests.post(xurl, headers=self.headers, data= request["postdata"])
                        '''
                        self.browser.load(xurl, method, self.headers, request["postdata"])
                        try:
                            content = self.browser.response.content 
                        except:
                            content =  self.browser.toHtml()
                        #content = self.browser.toHtml()
                        f = content.find(request["payload"])
                        self.browser.evaluate_js_file("/home/proxyscan/b0lu-fuzzle/plugins/dxss.js")
                        print request["payload"]
                        print "response content:---------------------------------------"
                        print content[:1000]
                        #print self.browser.response.content[:1000]
                        print "response headers:"
                        print self.browser.response.headers
                        print "-----------------------------"
                        #print "find pos=>"+str(f)
                        print ( "xss flag => %s"%str(self.browser.page.xss))
                        #print (Fore.Red+ "it is a test")
                    except Exception,e:
                        elog.exception(e)
                        
                    #f = re.findall(request["payload"], )
                    #print request["payload"]
                    #f = resp.content.find(request["payload"])
                    #f = self.__esm.query(resp.content)
                    #print resp.content
                    '''    
                    xss_post_data = {"url" : xurl,
                        "fuzzle_msg": xssPayloads.fuzzle_msg,
                        "headers" : str(resp.headers), 
                        "response" : str(resp.content),
                    }
                    resp = requests.post(self.xss_detect_server, data=xss_post_data)
                    xresult = resp.json()
                    if xresult["isVul"] and k not in self.vul_params:
                    '''
                    #if f != -1 or self.browser.page.xss:
                    if self.browser.page.xss or f != -1:
                    #if self.browser.page.xss :
                        if request["payload"] not in self.vpayloads:
                            self.vpayloads.append(request["payload"])
                        self.vul_params.append(k)
                        print "vul param:"+str(self.vul_params)
                        
        
        print "vul param:"+str(self.vul_params)

        self.dlog.debug("[ RXSSAudit Vul Result ] method: %s, parameter: %s, payload: %s"%(self.dreq.method, str(self.vul_params), self.vpayloads))
        if self.vul_params:
            vul = scanIssue(rid=self.dreq.rid, type= vulTypes.rxss, host= self.dreq.host, url= self.dreq.url, method=self.dreq.method, parameters=','.join(self.vul_params), payload= self.vpayloads )
            self.insertVul(vul)
        
        
def getPluginClass():
    return rxssAudit
                
if __name__ =='__main__':

    '''
    drequest = {
               "url" : "http://localhost/xss.php",
               "headers" : {},
               "postdata" : "name=zhangqin&passwd=dddd"
               }
    xss = rxssAudit(drequest)
    xss.audit()
    
    headers = {
        "Cookie": "security=low; PHPSESSID=f1rs4sm4bhjtgevnujl38lf7j4"
        }
    drequest = {
               "url" : "http://localhost/dvwa/vulnerabilities/xss_r/?name=ffff",
               "headers" : headers,
               #"postdata" : "name=zhangqin&passwd=dddd"
               "postdata" : ""
               }
    xss = rxssAudit(drequest)
    xss.audit()
    
    drequest = {
           "url" : "http://localhost/phpinfo.php?sss=ddd&ddd=ss&ddd=xxx&fff=sss",
           "headers" : {},
           "postdata" : ""
           }
    xss = rxssAudit(drequest)
    xss.audit()
    '''
    from utils.pluginsManager import pm
    from utils.GRedis import gredis
    from fuzzle.grequest import DRequest
    
    debug = 1

    if debug ==1:
        dreq = gredis.getTask() 
        print dreq        
        if dreq:
            dreq = DRequest(dreq)
            #print dreq
            xss = rxssAudit(dreq)
            xss.audit()
            #pm.run(dreq)
    elif debug == 2:
        drequest = """
        {"brequest":[71,69,84,32,40,109,108,59,113,61,48,46,57,44,42,47,42,59,113,61,48,46,56,13,10,65,99,99,101,112,116,45,76,97,110,103,117,97,103,101,58,32,122,104,45,67,78,44,122,104,59,113,61,48,46,56,44,101,110,45,85,83,59,113,61,48,46,53,44,101,110,59,113,61,48,46,51,13,10,65,99,99,101,112,116,45,69,110,99,111,100,105,110,103,58,32,103,122,105,112,44,32,100,101,102,108,97,116,101,13,10,88,45,70,111,114,119,97,114,100,101,100,45,70,111,114,58,32,56,46,56,46,56,46,56,13,10,67,111,110,110,101,99,116,105,111,110,58,32,107,101,101,112,45,97,108,105,118,101,13,10,80,114,97,103,109,97,58,32,110,111,45,99,97,99,104,101,13,10,67,97,99,104,101,45,67,111,110,116,114,111,108,58,32,110,111,45,99,97,99,104,101,13,10,13,10],"completed":true,"hasBodyParam":false,"hasCookieParam":false,"hasQueryStringParam":true,"hasSetCookies":false,"headers":["GET /gchatpic_new/4125232210/4125232210-2519897316-49DDAC0C4A168639B211526FE8757DA7/198?vuin=10461540&term=2%27;alert(/b0lu/);%27&cldver=5.7.2.2490&rf=naio&mType=picGd HTTP/1.1","Host: 123.138.148.150","User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)","Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding: gzip, deflate","X-Forwarded-For: 8.8.8.8","Connection: keep-alive","Pragma: no-cache","Cache-Control: no-cache"],"host":"123.138.148.150","method":"GET","postdata":"","protocol":"http","referrerURL":"","request":"GET /gchatpic_new/4125232210/4125232210-2519897316-49DDAC0C4A168639B211526FE8757DA7/198?vuin=10461540&term=2%27;alert(/b0lu/);%27&cldver=5.7.2.2490&rf=naio&mType=picGd HTTP/1.1\r\nHost: 123.138.148.150\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nX-Forwarded-For: 8.8.8.8\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\n\r\n","requestLength":5564,"requstContentType":"PNG","responseContentType":"image/png","responseContentType_burp":"PNG","responseInferredContentType_burp":"","responseLength":0,"responseTime":"","status":200,"targetPort":80,"url":"http://123.138.148.150:80/gchatpic_new/4125232210/4125232210-2519897316-49DDAC0C4A168639B211526FE8757DA7/198?vuin=10461540&term=2%27;alert(/b0lu/);%27&cldver=5.7.2.2490&rf=naio&mType=picGd","urlExtension":""}
        """
        print drequest 
        dreq = DRequest(drequest)
        xss = rxssAudit(drequest)
        xss.audit()






