#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from config.config import cf
from GLog import elog, getDlog
import os, MySQLdb, MySQLdb.cursors 


class GMysql(object):
    def __init__(self):
        self.dlog = getDlog(__name__)
        try:
            self.conn = MySQLdb.connect(host=cf.mysql_host ,user=cf.mysql_user ,passwd=cf.mysql_pass ,port=cf.mysql_port , db=cf.mysql_db,  charset='utf8')
            self.getCursor()
        except Exception, e:
            elog.exception(e)
        
    def getCursor(self):
        #cursorclass=MySQLdb.cursors.DictCursor,
        self.conn.autocommit(1) 
        self.cur=self.conn.cursor()
        
    def insertRequest(self, drequest):
        sql = "insert into requests( host, url, method, headers, cookies ,postdata, request, brequest) values( %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (drequest.host, drequest.url, drequest.method, str(drequest.headers), str(drequest.cookie) ,drequest.postdata, drequest.request, str(drequest.brequest))
        try:
            n = self.cur.execute(sql, params)
            if n==1:
                self.dlog.debug("[Mysql Insert] url:%s insert success"%drequest.url)
                return self.conn.insert_id()
            else:
                self.dlog.debug("[Mysql Insert] url:%s insert fail"%drequest.url)
        except Exception,e:
            elog.exception(e)
            
        #self.conn.insert_id()
        #self.cur.lastrowid
    
    def insertVul(self, scanissue):
        sql = "insert into vuls(rid, type, host, url, param, method, payloads) values(%s, %s, %s, %s, %s, %s, %s)"
        rid = int(scanissue.rid)
        params = ( rid, scanissue.type, scanissue.host, scanissue.url, str(scanissue.parameters), scanissue.method, str(scanissue.payload))
        try:
            n = self.cur.execute(sql, params)
            if n==1:
                self.dlog.debug("[Vul Insert] url:%s insert success"%scanissue.url)
            else:
                self.dlog.debug("[Vul Insert] url:%s insert fail"%scanissue.url)
        except Exception,e:
            elog.exception(e)
        
        
gm = GMysql()
if __name__ == '__main__':
    gm.insertRequest("")
    '''
    cur = gm.cur
    cur.execute('select * from vuls')
    rs = cur.fetchall()
    print rs
    sql = "insert into vuls(vid, type, host, url, param, method, payloads) values(1, 'sqli', 'test1', 'test1', 'test1', 'get', 'test1')"
    cur.execute(sql)
    '''